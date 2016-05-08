'''
Created on 07-May-2016

@author: bharat
'''
import xml.etree.ElementTree as ET
import pprint

xml_namespace_map = {
    "xs": "http://www.w3.org/2001/XMLSchema"
}

def parse_sequence_element(element, parent):
    return {parent.get("name") : [childelement.attrib for childelement in element.findall("xs:element", xml_namespace_map)]}

def parse_choice_element(element, parent):
    return {parent.get("name") : [childelement.attrib for childelement in element.findall("xs:element", xml_namespace_map)]}
       
complextype_funcdict = {"sequence": parse_sequence_element, "choice": parse_choice_element}

def parse_complex_type(element):    
    return [complextype_funcdict.get(x.tag[x.tag.find("}")+1:])(x, element) for x in element.getchildren() if complextype_funcdict.has_key(x.tag[x.tag.find("}")+1:])]

def parse_simple_type(elem, elemchild):
    return (elem.get("name"), elemchild.get("base")[len("xs:"):])

def gen_db_schema(xsdschema_filename, basetable_list):
    schema_generator = XSD2DBSchemaGenerator()
    schema_generator.gen_db_schema(xsdschema_filename, basetable_list)
    
class XSD2DBSchemaGenerator(object):

    def __init__(self, dbtype="Oracle", dbtype_func=None):
        self.simpletype_list = []
        self.complextype_list = []
        self.dbtype = dbtype
        self.dbtype_func = dbtype_func
    
    def process(self, key, value, displayname):        
        def parse_child(child_type):
            name = child_type.get("name")
            xmlType = child_type.get("type")
            
            if any([x for x in self.simpletype_list if x[0] == xmlType]):
                print(displayname+str(name))
            else:
                root_tables = [y for x in self.complextype_list for y in x for z in y if z in {xmlType} ]                
                [self.process(k, v,displayname+str(name)) for x in root_tables for k, v in x.iteritems()]                                
                    
        for x in value:
            parse_child(x) 
                  
    def gen_db_schema(self, xsdschema_filename, basetable_list):    
        tree = ET.parse(xsdschema_filename)
        root = tree.getroot()
            
        simpletype_list = root.findall("xs:simpleType", xml_namespace_map)
        
        complextype_list = root.findall("xs:complexType", xml_namespace_map)
        
        # db_type_func(elem.get("name"), elem_child.get("base")[len("xs:"):])
        
        self.simpletype_list = [parse_simple_type(elem, elem_child) for elem in simpletype_list for elem_child in elem.getchildren() if str(elem_child.tag).find("restriction")]
    
        self.complextype_list = [parse_complex_type(elem) for elem in complextype_list]                
        
        pprint.pprint(self.simpletype_list)
        
        pprint.pprint(self.complextype_list)
        
        root_tables = [y for x in self.complextype_list for y in x for key in y if key in basetable_list ]        
        
        [self.process(key, value, "") for x in root_tables for key, value in x.iteritems()]         
