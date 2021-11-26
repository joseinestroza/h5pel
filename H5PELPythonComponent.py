# -*- coding: utf-8 -*-

"""
    !This program is semi-PEP8 Compliant.

    @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
    @version 0.1.0p
    @date 2021/11/19

    !H5PEL Python Component: H5PEL Language translator (H5P Easy 
    !Language) for ".H5P" file creation, one-file-version.
    Copyright (C) 2021  José Inestroza
    !Created at Tegucigalpa, Honduras, C.A.

    This program is free for charge software: you can share it (copy and redistribute 
    the material in any medium or format) and/or modify it (remix, 
    transform, and build upon the material) under the terms of
    Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0), 
    under the following terms:

        Attribution — You must give appropriate credit, provide a link to the 
        license, and indicate if changes were made. You may do so in any reasonable 
        manner, but not in any way that suggests the licensor endorses you or your use.

        NonCommercial — You may not use the material for commercial purposes.

        ShareAlike — If you remix, transform, or build upon the material, you 
        must distribute your contributions under the same license as the original.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY. 

    https://creativecommons.org/licenses/by-nc-sa/4.0/

    !This project depends on Lark Parser. See Lark Parser Licence for more information.

    https://github.com/lark-parser/lark/blob/master/LICENSE
"""

import sys
import re
import random
import copy
import json as ujson
import subprocess
import datetime

from lark import Lark, Transformer, v_args 

@v_args(inline=True)
class Semantic(Transformer):
    """Processes every H5PEL text instruction.
    Uses NO-PURE functions. Verbose compliant.
    
        @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
        @version 0.1.0p
        @date 2021/11/19
    """

    def __init__(self):
        """Default values reservation."""
        self.presentation_name = None
        self.slides = None
        self.stack = []

    def to_string(self,value):
        """Removes quoting.

            Keyword arguments:
            value -- A quoted string
        """
        return value[1:-1]

    def presentationname(self,value):
        """Sets and informs about the presentation file name.

            Keyword arguments:
            value -- A quoted string
        """
        value = self.to_string(value)
        self.presentation_name = value
        print ("The presentation name is defined as: {}".format(value))

    def newslide(self,closing=False):
        """Closes the last open slide or creates a new one.

            Keyword arguments:
            closing -- It's a "closing slide" action or not
        """
        if not isinstance(self.slides,list):
            self.slides = []
        else:
            stack = self.stack
            self.slides.append(stack)
            self.stack = []
        if closing:
            print ("Last slide closed.")
        else:
            print ("Creates new slide.")

    def title(self,value):
        """Defines a new title.

            Keyword arguments:
            value -- A quoted string
        """
        if not isinstance(self.slides,list):
            self.newslide()
        value = self.to_string(value)
        self.stack.append("<h2>{}</h2>".format(value))
        print ("Creates new title: {}".format(value))

    def subtitle(self,value):
        """Defines a new subtitle.

            Keyword arguments:
            value -- A quoted string
        """
        if not isinstance(self.slides,list):
            self.newslide()
        value = self.to_string(value)
        self.stack.append("<h3>{}</h3>".format(value))
        print ("Creates new subtitle: {}".format(value))

    def paragraph(self,value):
        """Defines a new paragraph.

            Keyword arguments:
            value -- A quoted string
        """
        if not isinstance(self.slides,list):
            self.newslide()
        value = self.to_string(value)
        print ("Creates new paragraph: {}".format(value))
        self.stack.append("<p>{}</p>".format(value))

    def presentationwrite(self):
        """Creates a new presentation as a H5P file previous to ZIP."""
        self.newslide(True)
        presentation = H5P(self.presentation_name,self.slides)
        presentation.write()

class Reader:
    """Input reader from keyboard or piping.
    
        @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
        @version 0.1.0p
        @date 2021/11/19
    """

    def __init__(self): 
        pass

    def read(self):
        """Reads text from input."""
        self.text = []
        
        try:
            text = input()
            while True:
                self.text += [text]
                text = input()
        except EOFError:
            pass

        self.text = "\n".join(self.text)
        return self

class H5P:
    """Writes H5P files using H5P content resources.

        @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
        @version 0.1.0p
        @date 2021/11/19
    """

    def __init__(self,presentation_name,slides):
        """Default paths for H5P resources and default content definitions."""

        self.presentation_name = presentation_name

        self.temporal_file_name = "Resources/temp.temp"

        self.resources_path_H5P_json = "Resources/h5p.json"

        self.resources_path_course_presentation = "Resources/H5P.CoursePresentation-1.22"

        self.resources_path_content_json = "Resources/content/content.json"

        self.resources_path_content = "Resources/content"

        self.slides = slides

        self.h5pJson = {
            "title": self.presentation_name,
            "language": "und",
            "mainLibrary": "H5P.CoursePresentation",
            "embedTypes": ["div"],
            "license": "U",
            "defaultLanguage": "es",
            "preloadedDependencies": [{
                "machineName": "H5P.AdvancedText",
                "majorVersion": "1",
                "minorVersion": "1"
            }, {
                "machineName": "H5P.CoursePresentation",
                "majorVersion": "1",
                "minorVersion": "22"
            }, {
                "machineName": "FontAwesome",
                "majorVersion": "4",
                "minorVersion": "5"
            }, {
                "machineName": "H5P.JoubelUI",
                "majorVersion": "1",
                "minorVersion": "3"
            }, {
                "machineName": "H5P.Transition",
                "majorVersion": "1",
                "minorVersion": "0"
            }, {
                "machineName": "Drop",
                "majorVersion": "1",
                "minorVersion": "0"
            }, {
                "machineName": "Tether",
                "majorVersion": "1",
                "minorVersion": "0"
            }, {
                "machineName": "H5P.FontIcons",
                "majorVersion": "1",
                "minorVersion": "0"
            }]
        }

        self.content_json_slide_element_format = {
            "elements": [{
                "x": 3.2679738562091507,
                "y": 6.455305615685532,
                "width": 93.68191721132898,
                "height": 88.222510081035608,
                "action": {
                    "library": "H5P.AdvancedText 1.1",
                    "params": {
                        "text": None
                    },
                    "subContentId": self.generate_sub_content_id(),
                    "metadata": {
                        "contentType": "Text",
                        "license": "U",
                        "title": "Sin t\u00edtulo Text"
                    }
                },
                "alwaysDisplayComments": False,
                "backgroundOpacity": 0,
                "displayAsButton": False,
                "buttonSize": "big",
                "goToSlideType": "specified",
                "invisible": False,
                "solution": ""
            }],
            "slideBackgroundSelector": {}
        }

        self.content_json_format = {
            "presentation": {
                "slides": [],
                "keywordListEnabled": True,
                "globalBackgroundSelector": {},
                "keywordListAlwaysShow": False,
                "keywordListAutoHide": False,
                "keywordListOpacity": 90
            },
            "override": {
                "activeSurface": False,
                "hideSummarySlide": False,
                "summarySlideSolutionButton": True,
                "summarySlideRetryButton": True,
                "enablePrintButton": False,
                "social": {
                    "showFacebookShare": False,
                    "facebookShare": {
                        "url": "@currentpageurl",
                        "quote": "Yo obtuve @score de @maxScore en un trabajo en @currentpageurl."
                    },
                    "showTwitterShare": False,
                    "twitterShare": {
                        "statement": "Yo obtuve @score de @maxScore en un trabajo en @currentpageurl.",
                        "url": "@currentpageurl",
                        "hashtags": "h5p, course"
                    },
                    "showGoogleShare": False,
                    "googleShareUrl": "@currentpageurl"
                }
            },
            "l10n": {
                "slide": "Diapositiva",
                "score": "Puntaje",
                "yourScore": "Puntaje",
                "maxScore": "Puntaje m\u00e1ximo",
                "total": "Total",
                "totalScore": "Puntuaci\u00f3n Total",
                "showSolutions": "Mostrar soluci\u00f3n",
                "retry": "Reintentar",
                "exportAnswers": "Exportar com texto",
                "hideKeywords": "Ocultar lista de palabras claves",
                "showKeywords": "Mostrar lista de palabras claves",
                "fullscreen": "Pantalla completa",
                "exitFullscreen": "Salir de Pantalla completa",
                "prevSlide": "Diapositiva previa",
                "nextSlide": "Diapositiva siguiente",
                "currentSlide": "Diapositiva actual",
                "lastSlide": "Diapositiva final",
                "solutionModeTitle": "Salir del modo de soluci\u00f3n",
                "solutionModeText": "Modo de soluci\u00f3n",
                "summaryMultipleTaskText": "Actividades m\u00faltiples",
                "scoreMessage": "Obtuviste:",
                "shareFacebook": "Compartir en Facebook",
                "shareTwitter": "Compartir en Twitter",
                "shareGoogle": "Compartir en Google+",
                "summary": "Resumen",
                "solutionsButtonTitle": "Mostrar comentarios",
                "printTitle": "Imprimir",
                "printIngress": "Le gustar\u00eda imprimir esta presentaci\u00f3n?",
                "printAllSlides": "Imprimir todas las diapositivas",
                "printCurrentSlide": "Imprimir diapositiva actual",
                "noTitle": "Sin t\u00edtulo",
                "accessibilitySlideNavigationExplanation": "Use flecha izquierda y derecha para cambiar diapositiva en esa direcci\u00f3n siempre que est\u00e9 seleccionado el lienzo",
                "accessibilityCanvasLabel": "Lienzo de Presentaci\u00f3n. Use flechas izquierda y derecha para moverse entre diapositivas.",
                "containsNotCompleted": "@slideName contiene interacci\u00f3n no completada",
                "containsCompleted": "@slideName contiene interacci\u00f3n completada",
                "slideCount": "Diapositiva @index de @total",
                "containsOnlyCorrect": "@slideName solamente tiene respuestas correctas",
                "containsIncorrectAnswers": "@slideName tiene respuestas incorrectas",
                "shareResult": "Mostrar Resultado",
                "accessibilityTotalScore": "Usted obtuvo @score de @maxScore puntos en total",
                "accessibilityEnteredFullscreen": "Entr\u00f3 a pantalla completa",
                "accessibilityExitedFullscreen": "Sali\u00f3 de pantalla completa"
            }
        }
    
    def generate_sub_content_id(self):
        """Creates content id based con random caracter generation.
        
            @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
            @version 0.1.0p
            @date 2021/11/19
        """
        
        content_id = []
        code = []

        repeat = 8
        while repeat > 0:
            code.append(self.generate_random_caracter())
            repeat-=1
        content_id.append("".join(code))
        code = []

        repeat = 4
        while repeat > 0:
            code.append(self.generate_random_caracter())
            repeat-=1
        content_id.append("".join(code))
        code = []

        repeat = 4
        while repeat > 0:
            code.append(self.generate_random_caracter())
            repeat-=1
        content_id.append("".join(code))
        code = []

        repeat = 4
        while repeat > 0:
            code.append(self.generate_random_caracter())
            repeat-=1
        content_id.append("".join(code))
        code = []

        repeat = 12
        while repeat > 0:
            code.append(self.generate_random_caracter())
            repeat-=1
        content_id.append("".join(code))
        code = []
        
        return "-".join(content_id)

    def generate_random_caracter(self):
        """Random caracter generation.
        
            @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
            @version 0.1.0p
            @date 2021/11/19
        """

        if random.randint(0,1) == 0:
            return str(chr(random.randint(97,122)))
        return str(chr(random.randint(48,57)))

    def write_json(self,fileName,content):
        """Creates main json file for H5P.
        
            @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
            @version 0.1.0p
            @date 2021/11/19
        """

        f = open(fileName,"w")
        f.write(
            ujson.dumps(
                content, 
                indent=4
            )
        )
        f.close()

    def create_name_file_for_bash(self):
        """Defines the H5P file name and create a file, for bash, for zipping.
        
            @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
            @version 0.1.0p
            @date 2021/11/19
        """

        f = open(self.temporal_file_name,"w")
        f.write(
            "{}-{}.h5p".format(
                re.sub(' ', '-', 
                    re.sub('[^\w_.)( -]', '', self.presentation_name)
                ).lower(),
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            )
        )
        f.close()

    def write(self):
        """Writes the content and configurations H5P files for bash post usage.
        
            @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
            @version 0.1.0p
            @date 2021/11/19
        """

        slides = []
        for slide in self.slides:
            element = copy.deepcopy(self.content_json_slide_element_format)
            element["elements"][0]["action"]["params"]["text"] = "\n\n".join(slide)
            slides.append(element)
        content = copy.deepcopy(self.content_json_format)
        content["presentation"]["slides"] = slides
        
        self.write_json(self.resources_path_H5P_json,self.h5pJson)
        self.write_json(self.resources_path_content_json,content)
        
        print ("All resources have been created successfully.")
        print ("H5P configuration file path: {}".format(self.resources_path_H5P_json))
        print ("H5P content file path: {}".format(self.resources_path_content_json))
        
        self.create_name_file_for_bash()

        print ("H5PEL Python Component Done.")
        print ("Resources may be used by H5PEL Linux Bash Component for H5P file creation as a ZIP File.")

__grammar__ = """

    //@author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
    //@version 0.1.0p
    //@date 2021/11/19

    //Start axiom
    ?start: exp+

    //Allowed expressions
    ?exp: ( "name" | "begin" | "b" ) [(":" | "=")] string -> presentationname
        | ( "title" | "t" ) [(":" | "=")] string -> title
        | ( "subtitle" | "s" ) [(":" | "=")] string -> subtitle
        | ( "paragraph" | "p" ) [(":" | "=")] string -> paragraph
        | ( "new slide" | "new" | "n" ) -> newslide
        | ( "write" | "end" | "w" | "e" ) -> presentationwrite

    //String definition
    ?string: /"[^"]*"/
        | /'[^']*'/

    //Ignore spaces, new lines and tabs
    %ignore /\s+/
"""

if __name__ == '__main__':

    """Instance a reader."""
    reader = (Reader()).read()

    """Instance a Lark Parser."""
    parser = Lark(__grammar__,parser="lalr", transformer = Semantic())

    """Parse H5PEL as a language."""
    h5p_language_parser = parser.parse

    """Read text from input."""
    user_input_program = reader.text
    try:
        """Parse the input using the grammar with Lark."""
        h5p_language_parser(user_input_program)
    except Exception as e:
        """Throws error if detected."""
        print ("Error: %s" % e)