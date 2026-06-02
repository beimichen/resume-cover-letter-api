from weasyprint import Document, HTML
import io
import math
import os
import boto3
import re
import json
import logging

import cairocffi as cairo
from weasyprint.draw import draw_page, stacked
from weasyprint.logger import LOGGER, PROGRESS_LOGGER
from weasyprint.pdf import write_pdf_metadata

logger = logging.getLogger(__name__)


class CustomDocument(Document):

    def _w3c_date_to_iso(string, attr_name):
        """Tranform W3C date to ISO-8601 format."""
        if string is None:
            return None
        match = W3C_DATE_RE.match(string)
        if match is None:
            LOGGER.warning('Invalid %s date: %r', attr_name, string)
            return None
        groups = match.groupdict()
        iso_date = '%04i-%02i-%02iT%02i:%02i:%02i' % (
            int(groups['year']),
            int(groups['month'] or 1),
            int(groups['day'] or 1),
            int(groups['hour'] or 0),
            int(groups['minute'] or 0),
            int(groups['second'] or 0))
        if groups['hour']:
            assert groups['minute']
            if groups['tz_hour']:
                assert groups['tz_hour'].startswith(('+', '-'))
                assert groups['tz_minute']
                iso_date += '%+03i:%02i' % (
                    int(groups['tz_hour']), int(groups['tz_minute']))
            else:
                iso_date += '+00:00'
        return iso_date

    def write_pdf_html(self, target=None, zoom=1, attachments=None,
                               data_type=None):
        """Paint the pages in a PDF file, with meta-data.

        PDF files written directly by cairo do not have meta-data such as
        bookmarks/outlines and hyperlinks.

        :type target: str, pathlib.Path or file object
        :param target:
            A filename where the PDF file is generated, a file object, or
            :obj:`None`.
        :type zoom: float
        :param zoom:
            The zoom factor in PDF units per CSS units.  **Warning**:
            All CSS units are affected, including physical units like
            ``cm`` and named sizes like ``A4``.  For values other than
            1, the physical CSS units will thus be "wrong".
        :type attachments: list
        :param attachments: A list of additional file attachments for the
            generated PDF document or :obj:`None`. The list's elements are
            :class:`Attachment` objects, filenames, URLs or file-like objects.
        :returns:
            The PDF as :obj:`bytes` if ``target`` is not provided or
            :obj:`None`, otherwise :obj:`None` (the PDF is written to
            ``target``).

        """

        # 0.75 = 72 PDF point (cairo units) per inch / 96 CSS pixel per inch
        scale = zoom * 0.75
        # Use an in-memory buffer, as we will need to seek for
        # metadata. Directly using the target when possible doesn't
        # significantly save time and memory use.
        file_obj = io.BytesIO()
        # (1, 1) is overridden by .set_size() below.
        surface = cairo.PDFSurface(file_obj, 1, 1)
        context = cairo.Context(surface)

        PROGRESS_LOGGER.info('Step 6 - Drawing')

        paged_links_and_anchors = list(self.resolve_links())
        for page, links_and_anchors in zip(
                self.pages, paged_links_and_anchors):
            links, anchors = links_and_anchors
            surface.set_size(
                math.floor(scale * (
                    page.width + page.bleed['left'] + page.bleed['right'])),
                math.floor(scale * (
                    page.height + page.bleed['top'] + page.bleed['bottom'])))
            with stacked(context):
                context.translate(
                    page.bleed['left'] * scale, page.bleed['top'] * scale)
                page.paint(context, scale=scale)
                self.add_hyperlinks(links, anchors, context, scale)
                surface.show_page()

        PROGRESS_LOGGER.info('Step 7 - Adding PDF metadata')

        # TODO: overwrite producer when possible in cairo
        if cairo.cairo_version() >= 11504:
            # Set document information
            for attr, key in (
                    ('title', cairo.PDF_METADATA_TITLE),
                    ('description', cairo.PDF_METADATA_SUBJECT),
                    ('generator', cairo.PDF_METADATA_CREATOR)):
                value = getattr(self.metadata, attr)
                if value is not None:
                    surface.set_metadata(key, value)
            for attr, key in (
                    ('authors', cairo.PDF_METADATA_AUTHOR),
                    ('keywords', cairo.PDF_METADATA_KEYWORDS)):
                value = getattr(self.metadata, attr)
                if value is not None:
                    surface.set_metadata(key, ', '.join(value))
            for attr, key in (
                    ('created', cairo.PDF_METADATA_CREATE_DATE),
                    ('modified', cairo.PDF_METADATA_MOD_DATE)):
                value = getattr(self.metadata, attr)
                if value is not None:
                     surface.set_metadata(key, self._w3c_date_to_iso(value, attr))

            # Set bookmarks
            bookmarks = self.make_bookmark_tree()
            levels = [cairo.PDF_OUTLINE_ROOT] * len(bookmarks)
            while bookmarks:
                bookmark = bookmarks.pop(0)
                title = bookmark.label
                destination = bookmark.destination
                children = bookmark.children
                state = bookmark.state
                page, x, y = destination

                # We round floats to avoid locale problems, see
                # https://github.com/Kozea/WeasyPrint/issues/742
                link_attribs = 'page={} pos=[{} {}]'.format(
                    page + 1, int(round(x * scale)),
                    int(round(y * scale)))

                outline = surface.add_outline(
                    levels.pop(), title, link_attribs,
                    cairo.PDF_OUTLINE_FLAG_OPEN if state == 'open' else 0)
                levels.extend([outline] * len(children))
                bookmarks = children + bookmarks

        surface.finish()

        # Add extra PDF metadata: attachments, embedded files
        attachment_links = [
            [link for link in page_links if link[0] == 'attachment']
            for page_links, page_anchors in paged_links_and_anchors]
        # Write extra PDF metadata only when there is a least one from:
        # - attachments in metadata
        # - attachments as function parameters
        # - attachments as PDF links
        # - bleed boxes
        condition = (
            self.metadata.attachments or
            attachments or
            any(attachment_links) or
            any(any(page.bleed.values()) for page in self.pages))
        if condition:
            write_pdf_metadata(
                file_obj, scale, self.url_fetcher,
                self.metadata.attachments + (attachments or []),
                attachment_links, self.pages)

            return file_obj


CustomDocuent = CustomDocument


class CustomHTML(HTML):

    def render(self, stylesheets=None, enable_hinting=False,
               presentational_hints=False, font_config=None):
        """Lay out and paginate the document, but do not (yet) export it
        to PDF or PNG.

        This returns a :class:`~document.Document` object which provides
        access to individual pages and various meta-data.
        See :meth:`write_pdf` to get a PDF directly.

        .. versionadded:: 0.15

        :type stylesheets: list
        :param stylesheets:
            An optional list of user stylesheets. List elements are
            :class:`CSS` objects, filenames, URLs, or file
            objects. (See :ref:`stylesheet-origins`.)
        :type enable_hinting: bool
        :param enable_hinting:
            Whether text, borders and background should be *hinted* to fall
            at device pixel boundaries. Should be enabled for pixel-based
            output (like PNG) but not for vector-based output (like PDF).
        :type presentational_hints: bool
        :param presentational_hints: Whether HTML presentational hints are
            followed.
        :type font_config: :class:`~fonts.FontConfiguration`
        :param font_config: A font configuration handling ``@font-face`` rules.
        :returns: A :class:`~document.Document` object.

        """
        return CustomDocument._render(
            self, stylesheets, enable_hinting, presentational_hints,
            font_config)

    def write_pdf_html(self, target=None, stylesheets=None, zoom=1,
                               attachments=None, presentational_hints=False,
                               font_config=None, data_type=None):
        return self.render(
            stylesheets, enable_hinting=False,
            presentational_hints=presentational_hints,
            font_config=font_config).write_pdf_html(
            target, zoom, attachments, data_type)


W3C_DATE_RE = re.compile('''
    ^
    [ \t\n\f\r]*
    (?P<year>\\d\\d\\d\\d)
    (?:
        -(?P<month>0\\d|1[012])
        (?:
            -(?P<day>[012]\\d|3[01])
            (?:
                T(?P<hour>[01]\\d|2[0-3])
                :(?P<minute>[0-5]\\d)
                (?:
                    :(?P<second>[0-5]\\d)
                    (?:\\.\\d+)?  # Second fraction, ignored
                )?
                (?:
                    Z |  # UTC
                    (?P<tz_hour>[+-](?:[01]\\d|2[0-3]))
                    :(?P<tz_minute>[0-5]\\d)
                )
            )?
        )?
    )?
    [ \t\n\f\r]*
    $
''', re.VERBOSE)