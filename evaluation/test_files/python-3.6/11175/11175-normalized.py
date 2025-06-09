def qrcode(cls, data, mode='base64', version=None, error_correction='L', box_size=10, border=0, fit=True, fill_color='black', back_color='white', **kwargs):
    """Makes qr image using qrcode as qrc. See documentation
        for qrcode (https://pypi.python.org/pypi/qrcode) package for more info.

        :param data: String data.
        :param mode: Output mode, [base64|raw].
        :param version: The size of the QR Code (1-40).
        :param error_correction: The error correction used for the QR Code.
        :param box_size: The number of pixels for each "box" of the QR code.
        :param border: The number of box for border.
        :param fit: If `True`, find the best fit for the data.
        :param fill_color: Frontend color.
        :param back_color: Background color.

        :param icon_img: Small icon image name or url.
        :param factor: Resize for icon image (default: 4, one-fourth of QRCode)
        :param icon_box: Icon image position [left, top] (default: image center)
        """
    qr = qrc.QRCode(version=version, error_correction=cls.correction_levels[error_correction], box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=fit)
    fcolor = fill_color if fill_color.lower() in cls.color or fill_color.startswith('#') else '#' + fill_color
    bcolor = back_color if back_color.lower() in cls.color or back_color.startswith('#') else '#' + back_color
    out = BytesIO()
    qr_img = qr.make_image(back_color=bcolor, fill_color=fcolor)
    qr_img = qr_img.convert('RGBA')
    qr_img = cls._insert_img(qr_img, **kwargs)
    qr_img.save(out, 'PNG')
    out.seek(0)
    if mode == 'base64':
        return u'data:image/png;base64,' + base64.b64encode(out.getvalue()).decode('ascii')
    elif mode == 'raw':
        return out