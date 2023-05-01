"""Not yet implemented."""
from ..osascript import OSAObjProxy

# class Text(OSAObjProxy):
#     def __init__(self, item_ref):
#         super().__init__(item_ref)

#     # elements
#     @property
#     def attachments(self) -> List[Attachment]:
#         """List of the attachments contained in the text."""
#         return self.get_element_array('attachment')

#     @property
#     def attribute_runs(self) -> List[AttributeRun]:
#         """List of attribute runs containing formatting information for portions of the text."""
#         return self.get_element_array('attributeRun')

#     @property
#     def characters(self) -> List[str]:
#         """List of the individual characters in the text."""
#         return self.get_element_array('character')

#     @property
#     def paragraphs(self) -> List[Paragraph]:
#         """List of paragraphs contained in the text."""
#         return self.get_element_array('paragraph')

#     @property
#     def words(self) -> List[Word]:
#         """List of words contained in the text."""
#         return self.get_element_array('word')

#     # properties
#     @property
#     def color(self) -> Color:
#         """The color of the first character."""
#         return self.get_property('color', Color)

#     @color.setter
#     def color(self, value: Color):
#         self.set_property('color', value)

#     @property
#     def font(self) -> Text:
#         """The name of the font of the first character."""
#         return self.get_property_native('font')

#     @font.setter
#     def font(self, value: Text):
#         self.set_property('font', value)

#     @property
#     def size(self) -> int:
#         """The size in points of the first character."""
#         return self.get_property('size', int)

#     @size.setter
#     def size(self, value: int):
#         self.set_property('size', value)

# OSAObjProxy._NAME_CLASS_MAP['text'] = Text