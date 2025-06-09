from odoo import fields, models

class TicketBAIVATRegimeKey(models.Model):
    """
    SII_FAQs_version_1.1_11_sept_2019.pdf
                                        Claves compatibles

    07 - Régimen especial criterio de caja
                                01 - Régimen general
                                03 - REBU
                                05 – Régimen especial de agencias de viajes
                                12 - Arrendamiento local de negocios

    05 - Régimen especial de agencias de viaje
                                01- Régimen general
                                06 - Régimen especial grupo de IVA nivel avanzado
                                07 – Régimen especial criterio de caja
                                08 - Operaciones sujetas a IGIC, IPSI
                                12 - Arrendamiento local de negocios

    12 - Arrendamiento
                                05 – Régimen especial de agencias de viajes
                                06 - Régimen especial grupo de IVA nivel avanzado
                                07 – Régimen especial criterio de caja
                                08 - Operaciones sujetas a IGIC, IPSI
    03 - REBU
                                01 - Régimen general
    01 - Régimen general
                                08 - Operaciones sujetas a IGIC, IPSI

    * La clave 07 (Criterio de caja) siempre debe ser la primera clave a informar.
    * La clave 05 (Agencias de viajes) debe ser la primera clave a informar salvo que
    concurra con la clave 07 (Criterio de caja).
    * La clave 06 (Régimen especial grupo de entidades en IVA-nivel avanzado) debe ser
    la primera clave a informar cuando concurra con la clave 12.
    * La clave 03 (Régimen especial de bienes usados, objetos de arte, antigüedades y
    objetos de colección) debe ser la primera clave a informar cuando concurra con la
    clave 01.
    """
    _name = 'tbai.vat.regime.key'
    _description = 'TicketBAI VAT Regime mapping keys'
    code = fields.Char(string='Code', required=True)
    name = fields.Char('Name', required=True)

    def name_get(self):
        vals = []
        for record in self:
            name = '[{}]-{}'.format(record.code, record.name)
            vals.append(tuple([record.id, name]))
        return vals