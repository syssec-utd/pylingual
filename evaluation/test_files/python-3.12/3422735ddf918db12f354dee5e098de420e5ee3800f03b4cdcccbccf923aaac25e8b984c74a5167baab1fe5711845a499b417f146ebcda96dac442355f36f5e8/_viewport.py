import ovito
from . import Viewport
from ..nonpublic import RenderSettings, FrameBuffer, OpenGLViewportWindow, SceneRenderer

def _Viewport_render_image(self, size=(640, 480), frame=0, filename=None, background=(1.0, 1.0, 1.0), alpha=False, renderer=None, crop=False, layout=None):
    """ Renders an image of the viewport's view.

        :param size: A pair of integers specifying the horizontal and vertical dimensions of the output image in pixels.
        :param int frame: The animation frame to render. Numbering starts at 0. See the :py:attr:`FileSource.num_frames <ovito.pipeline.FileSource.num_frames>` property for the number of loaded animation frames.
        :param str filename: The file path under which the rendered image should be saved (optional).
                             Supported output formats are: :file:`.png`, :file:`.jpeg` and :file:`.tiff`.
        :param background: A triplet of RGB values in the range [0,1] specifying the background color of the rendered image.
        :param alpha: This option makes the background transparent so that the rendered image may later be superimposed on a different backdrop.
                      When using this option, make sure to save the image in the PNG format in order to preserve the generated transparency information.
        :param renderer: The rendering engine to use. If set to ``None``, either OpenGL or Tachyon are used,
                         depending on the availability of OpenGL in the current execution context.
        :param crop: This option cuts away border areas of the rendered image filled with the background color; the resulting image may thus turn out smaller than the requested *size*. 
        :param layout: Optional definition of a multi-viewport layout to be rendered into the output image. The layout must be provided as a list of :py:class:`Viewport` objects
                       and corresponding rectangular areas, which determine where each viewport's picture appears within the composed output image. 
                       Please make use of OVITO Pro's :ref:`code generation <manual:python_code_generation>` function to learn how to construct the *layout* argument. 
        :returns: A `QImage <https://doc.qt.io/qtforpython/PySide6/QtGui/QImage.html>`__ object containing the rendered picture.

        **Populating the scene**

        Before rendering an image using this method, you should make sure the three-dimensional contains some
        visible objects. Typically this involves calling the :py:meth:`Pipeline.add_to_scene() <ovito.pipeline.Pipeline.add_to_scene>`
        method on a pipeline to insert its output data into the scene::

           pipeline = import_file('simulation.dump')
           pipeline.add_to_scene()

        **Selecting the rendering backend**

        OVITO supports several different rendering backends for producing pictures of the three-dimensional scene:

            * :py:class:`OpenGLRenderer` (default)
            * :py:class:`TachyonRenderer`
            * :py:class:`OSPRayRenderer`

        Each of these backends exhibits specific parameters that control the image quality and other aspect of the image
        generation process. Typically, you would create an instance of one of these renderer classes, configure it and pass
        it to the :py:meth:`!render_image()` method:

        .. literalinclude:: ../example_snippets/viewport_select_renderer.py
           :lines: 5-

        **Post-processing images**

        If the ``filename`` parameter is omitted, the method does not save the rendered image to disk.
        This gives you the opportunity to paint additional graphics on top before saving the
        `QImage <https://doc.qt.io/qtforpython/PySide6/QtGui/QImage.html>`__ later using its ``save()`` method:

        .. literalinclude:: ../example_snippets/render_to_image.py

        As an alternative to the direct method demonstrated above, you can also make use of a :py:class:`PythonViewportOverlay`
        to paint custom graphics on top of rendered images.
    """
    assert len(size) == 2 and size[0] > 0 and (size[1] > 0)
    assert len(background) == 3
    assert background[0] >= 0.0 and background[0] <= 1.0
    assert background[1] >= 0.0 and background[1] <= 1.0
    assert background[2] >= 0.0 and background[2] <= 1.0
    assert renderer is None or isinstance(renderer, SceneRenderer)
    rs = RenderSettings()
    rs.output_image_width, rs.output_image_height = size
    rs.background_color = background
    rs.generate_alpha = alpha
    if renderer is not None:
        rs.renderer = renderer
    rs.range = RenderSettings.Range.CustomFrame
    rs.custom_frame = int(frame)
    if layout is None:
        layout = [(self, (0.0, 0.0, 1.0, 1.0))]
    if self.scene is None:
        raise RuntimeError('Cannot render viewport which has no scene set.')
    if len(self.scene.children) == 0:
        print('Warning: The scene to be rendered is empty. Did you forget to add a pipeline to the scene using Pipeline.add_to_scene()?')
    fb = rs.render_scene(self.scene.anim, layout)
    if crop:
        fb.auto_crop()
    img = fb.image
    if filename and (not img.save(filename)):
        raise RuntimeError(f"Failed to save rendered image to output file '{filename}'")
    return img
Viewport.render_image = _Viewport_render_image

def _Viewport_render_anim(self, filename, size=(640, 480), fps=10, background=(1.0, 1.0, 1.0), renderer=None, range=None, every_nth=1, layout=None):
    """ Renders an animation sequence.

        :param str filename: The filename under which the rendered animation should be saved.
                             Supported video formats are: :file:`.avi`, :file:`.mp4`, :file:`.mov` and :file:`.gif`.
                             Alternatively, an image format may be specified (:file:`.png`, :file:`.jpeg`).
                             In this case, a series of image files will be produced, one for each frame, which
                             may be combined into an animation using an external video encoding tool of your choice.
        :param size: The resolution of the movie in pixels.
        :param fps: The number of frames per second of the encoded movie. This determines the playback speed of the animation.
        :param background: An RGB triplet in the range [0,1] specifying the background color of the rendered movie.
        :param renderer: The rendering engine to use. If none is specified, either OpenGL or Tachyon are used,
                         depending on the availability of OpenGL in the script execution context.
        :param range: The interval of frames to render, specified in the form ``(from,to)``.
                      Frame numbering starts at 0. If no interval is specified, the entire animation is rendered, i.e.
                      frame 0 through (:py:attr:`FileSource.num_frames <ovito.pipeline.FileSource.num_frames>`-1).
        :param every_nth: Frame skipping interval in case you don't want to render every frame of a very long animation.
        :param layout: Optional definition of a multi-viewport layout to be rendered into the output image. 

        See also the :py:meth:`.render_image` method for a more detailed discussion of some of these parameters.
    """
    assert len(size) == 2 and size[0] > 0 and (size[1] > 0)
    assert fps >= 1
    assert every_nth >= 1
    assert len(background) == 3
    assert background[0] >= 0.0 and background[0] <= 1.0
    assert background[1] >= 0.0 and background[1] <= 1.0
    assert background[2] >= 0.0 and background[2] <= 1.0
    assert renderer is None or isinstance(renderer, SceneRenderer)
    rs = RenderSettings()
    rs.output_image_width, rs.output_image_height = size
    rs.background_color = background
    rs.output_filename = str(filename)
    rs.save_to_file = True
    rs.frames_per_second = int(fps)
    if renderer:
        rs.renderer = renderer
    rs.every_nth_frame = int(every_nth)
    if range:
        rs.range = RenderSettings.Range.CustomInterval
        rs.custom_range_start, rs.custom_range_end = range
    else:
        rs.range = RenderSettings.Range.Animation
    if layout is None:
        layout = [(self, (0.0, 0.0, 1.0, 1.0))]
    if self.scene is None:
        raise RuntimeError('Cannot render viewport which has no scene set.')
    if len(self.scene.children) == 0:
        print('Warning: The scene to be rendered is empty. Did you forget to add a pipeline to the scene using Pipeline.add_to_scene()?')
    rs.render_scene(self.scene.anim, layout)
Viewport.render_anim = _Viewport_render_anim

def _Viewport_zoom_all(self, size=(640, 480)):
    """ Repositions the viewport camera such that all objects in the scene become completely visible.
        The current orientation (:py:attr:`camera_dir`) of the viewport's camera is maintained but
        the :py:attr:`camera_pos` and :py:attr:`fov` parameters are adjusted by this method.

        :param size: Size in pixels of the image that is going to be renderer from this viewport.
                     This information is used to compute the aspect ratio of the viewport rectangle into which 
                     the visible objects should be fitted. The tuple should match the *size* argument being passed
                     to :py:meth:`render_image`.

        Note that this method uses an axis-aligned bounding box computed at frame 0 of the
        loaded trajectory enclosing all visible objects to adjust the viewport camera. 
        Make sure to call :py:meth:`Pipeline.add_to_scene() <ovito.pipeline.Pipeline.add_to_scene>` first 
        to insert some visible object(s) into the scene.
    """
    assert len(size) == 2 and size[0] > 0 and (size[1] > 0)
    aspect_ratio = size[1] / size[0]
    self._zoomToSceneExtents(aspect_ratio)
Viewport.zoom_all = _Viewport_zoom_all

def _Viewport_create_qt_widget(self, parent=None):
    """
    Creates an interactive visual widget displaying the three-dimensional scene as seen through this virtual viewport.
    The method creates an interactive window accepting mouse inputs from the user similar to the viewport windows 
    of the OVITO desktop application. You can use this method to develop custom user interfaces based on the Qt cross-platform framework
    that integrate OVITO's functionality and display the output of a data pipeline.

    :param parent: An optional Qt widget that should serve as parent of the newly created viewport widget. 
    :returns: A new `QWidget <https://doc.qt.io/qtforpython/PySide6/QtWidgets/QWidget.html>`__ displaying the three-dimensional scene as seen through the virtual viewport.

    The Qt widget returned by this method is linked to this :py:class:`!Viewport` instance. 
    Any changes your Python script subsequently makes to the non-visual :py:class:`!Viewport` instance,
    for example setting :py:attr:`camera_pos` or :py:attr:`camera_dir`, will automatically be reflected by the 
    visual viewport widget. Vice versa will interactions of the user with the viewport widget
    automatically lead to changes of the corresponding fields of the :py:class:`!Viewport` instance.

    The following short example program demonstrates the use of the :py:meth:`!create_qt_widget` method. Please see the 
    `Qt for Python <https://doc.qt.io/qtforpython/>`__ documentation for more information on how to create graphical 
    user interfaces using the Qt framework.

    .. literalinclude:: ../example_snippets/viewport_create_widget.py
        :lines: 22-

    """
    from ovito.qt_compat import shiboken
    from ovito.qt_compat import QtWidgets
    assert parent is None or isinstance(parent, QtWidgets.QWidget)
    show_viewport_title = False
    vpwin_ptr = OpenGLViewportWindow._create(self, 0 if parent is None else shiboken.getCppPointer(parent)[0], show_viewport_title)
    return shiboken.wrapInstance(vpwin_ptr, QtWidgets.QWidget)
Viewport.create_qt_widget = _Viewport_create_qt_widget
Viewport.create_widget = lambda self, parent=None: self.create_qt_widget(parent)