import pytest
import math
from ezdxf.entities.line import Line
from ezdxf.lldxf.const import DXF12, DXF2000, DXFValueError
from ezdxf.lldxf.tagwriter import TagCollector, basic_tags_from_text
from ezdxf.math import Matrix44
TEST_CLASS = Line
TEST_TYPE = 'LINE'
ENTITY_R12 = '0\nLINE\n5\n0\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n1.0\n21\n1.0\n31\n1.0\n'
ENTITY_R2000 = '0\nLINE\n5\n0\n330\n0\n100\nAcDbEntity\n8\n0\n100\nAcDbLine\n10\n0.0\n20\n0.0\n30\n0.0\n11\n1.0\n21\n1.0\n31\n1.0\n'

@pytest.fixture(params=[ENTITY_R12, ENTITY_R2000])
def line(request):
    return Line.from_text(request.param)

def test_registered():
    from ezdxf.entities.factory import ENTITY_CLASSES
    assert TEST_TYPE in ENTITY_CLASSES

def test_default_init():
    entity = Line()
    assert entity.dxftype() == TEST_TYPE

def test_default_new():
    entity = Line.new(handle='ABBA', owner='0', dxfattribs={'color': '7', 'start': (1, 2, 3), 'end': (4, 5, 6)})
    assert entity.dxf.layer == '0'
    assert entity.dxf.color == 7
    assert entity.dxf.start == (1, 2, 3)
    assert entity.dxf.start.x == 1, 'is not Vec3 compatible'
    assert entity.dxf.start.y == 2, 'is not Vec3 compatible'
    assert entity.dxf.start.z == 3, 'is not Vec3 compatible'
    assert entity.dxf.end == (4, 5, 6)
    assert entity.dxf.extrusion == (0.0, 0.0, 1.0)
    assert entity.dxf.hasattr('extrusion') is False, 'just the default value'
    entity.dxf.shadow_mode = 1
    assert entity.dxf.shadow_mode == 1

def test_load_from_text(line):
    assert line.dxf.layer == '0'
    assert line.dxf.color == 256, 'default color is 256 (by layer)'
    assert line.dxf.start == (0, 0, 0)
    assert line.dxf.end == (1, 1, 1)

@pytest.mark.parametrize('txt,ver', [(ENTITY_R2000, DXF2000), (ENTITY_R12, DXF12)])
def test_write_dxf(txt, ver):
    expected = basic_tags_from_text(txt)
    line = TEST_CLASS.from_text(txt)
    collector = TagCollector(dxfversion=ver, optional=True)
    line.export_dxf(collector)
    assert collector.tags == expected
    collector2 = TagCollector(dxfversion=ver, optional=False)
    line.export_dxf(collector2)
    assert collector.has_all_tags(collector2)

def test_get_pass_through_ocs():
    line = Line.new(dxfattribs={'start': (0, 0, 0), 'end': (1, 0, 0), 'extrusion': (0, 0, -1)})
    ocs = line.ocs()
    assert ocs.to_wcs((0, 0, 0)) == (0, 0, 0)
    assert ocs.to_wcs((1, 0, 0)) == (1, 0, 0)

def test_transform():
    line = Line.new(dxfattribs={'start': (0, 0, 0), 'end': (1, 0, 0), 'extrusion': (0, 1, 0)})
    m = Matrix44.translate(1, 2, 3)
    line.transform(m)
    assert line.dxf.start == (1, 2, 3)
    assert line.dxf.end == (2, 2, 3)
    assert line.dxf.extrusion == (0, 1, 0)
    new_line = line.copy()
    new_line.transform(m)
    assert new_line.dxf.start == (2, 4, 6)
    assert new_line.dxf.end == (3, 4, 6)
    assert new_line.dxf.extrusion == (0, 1, 0)

def test_translation():
    line = Line.new(dxfattribs={'start': (0, 0, 0), 'end': (1, 0, 0), 'extrusion': (0, 1, 0)})
    line.translate(1, 2, 3)
    assert line.dxf.start == (1, 2, 3)
    assert line.dxf.end == (2, 2, 3)

def test_rotation():
    line = Line.new(dxfattribs={'start': (0, 0, 0), 'end': (1, 0, 0), 'extrusion': (0, 1, 0)})
    angle = math.pi / 4
    m = Matrix44.z_rotate(angle)
    line.transform(m)
    assert line.dxf.start == (0, 0, 0)
    assert line.dxf.end.isclose((math.cos(angle), math.sin(angle), 0), abs_tol=1e-09)
    assert line.dxf.extrusion.isclose((-math.cos(angle), math.sin(angle), 0), abs_tol=1e-09)
    assert line.dxf.thickness == 0

def test_scaling():
    line = Line.new(dxfattribs={'start': (0, 0, 0), 'end': (1, 0, 0), 'extrusion': (0, 1, 0), 'thickness': 2})
    m = Matrix44.scale(2, 2, 0)
    line.transform(m)
    assert line.dxf.start == (0, 0, 0)
    assert line.dxf.end == (2, 0, 0)
    assert line.dxf.extrusion == (0, 1, 0)
    assert line.dxf.thickness == 4

def test_copy_entity_transparency():
    line = Line()
    line2 = line.copy()
    assert line2.dxf.hasattr('transparency') is False
    line.transparency = 0.5
    line2 = line.copy()
    assert line2.dxf.transparency == 33554559

def test_setting_invalid_transparency_value_raises_exception():
    line = Line()
    with pytest.raises(DXFValueError):
        line.dxf.transparency = 0

def test_load_entity_with_invalid_transparency():
    line = Line.from_text(ENTITY_INVALID_TRANSPARENCY)
    assert line.dxf.transparency == 268435456
    assert line.transparency == 0.0, 'should replace invalid transparency by opaque'
ERR_LINE = '0\nLINE\n5\n0\n330\n0\n100\nAcDbEntity\n100\nAcDbLine\n8\n0\n62\n1\n6\nLinetype\n10\n0.0\n20\n0.0\n30\n0.0\n11\n1.0\n21\n1.0\n31\n1.0\n'
ENTITY_INVALID_TRANSPARENCY = '0\nLINE\n5\n0\n330\n0\n100\nAcDbEntity\n8\n0\n440\n268435456\n100\nAcDbLine\n10\n0.0\n20\n0.0\n30\n0.0\n11\n1.0\n21\n1.0\n31\n1.0\n'

def test_recover_acdb_entity_tags():
    line = Line.from_text(ERR_LINE)
    assert line.dxf.layer == '0'
    assert line.dxf.color == 1
    assert line.dxf.linetype == 'Linetype'
MALFORMED_LINE = '0\nLINE\n5\n0\n62\n7\n330\n0\n6\nLT_EZDXF\n8\nLY_EZDXF\n100\nAcDbEntity\n10\n1.0\n20\n1.0\n30\n1.0\n100\nAcDbLine\n11\n2.0\n21\n2.0\n31\n2.0\n100\nAcDbInvalidSubclass\n'

def test_malformed_line():
    line = Line.from_text(MALFORMED_LINE)
    assert line.dxf.layer == 'LY_EZDXF'
    assert line.dxf.linetype == 'LT_EZDXF'
    assert line.dxf.color == 7
    assert line.dxf.start.isclose((1, 1, 1))
    assert line.dxf.end.isclose((2, 2, 2))