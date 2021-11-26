# H5PEL Language Interpreter/Translator

   H5PEL (H5P Easy Language) is a markup language for creating H5P presentations (https://h5p.org). This public H5PEL version (named v0.1.0p) is based on Lark (https://github.com/lark-parser/lark), a parsing toolkit built for Python.

   The etymology of H5PEL (pronounced "haspel") comes from "H5P" which is the name of the tool that it is built for and "EL" that stands for "Easy Language".  

   This first public version is just the initial step in the evolution of H5PEL, but it's not a community based project (yet), so it doesn't have a development road map as of today.

**Who is it for?**

   - **Teachers/Coders/Programmers**: build H5P web presentations fast by using a markup language, that allows basic titles and paragraphs components and admits the use of HTML5 if you want to (like unordered lists, bold, italics, etc). Its language supports different reserved words for the same semantics. See the grammar below. 

   - **Students**: H5PEL is based in Lark which is used in Computer Science in some programming languages courses at undergrad level. Lark is used by H5PEL creator when teaching a course called "IS-513 Programming Languages", at the System Engineering Department, in the National Autonomous University of Honduras.

   - **Enthusiasts**: it's for everyone who likes computer science, basic programming  and any related areas of knowledge.

# H5PEL Grammar

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

# How to create my first sample

   Download the H5PEL public version on your computer using the GitHub download button and then use the **run.sh** file in a terminal emulator on a GNU/Linux operating system for creating your first H5P presentation using H5PEL. You'll need to install a Python 3.x version on your system for H5PEL and Lark v1.0.0a to work. Use the **sample.h5pel** as the input file and the interpreter will create a output file using the name parameter defined inside the input file.

      $ sh run.sh sample.h5pel

**Input file sample**

      begin "H5PEL - Language for the Generation of H5P Course Presentation"

         title "H5P"

         paragraph "H5P Presentations, known as <strong> Course Presentation </strong> by its English name, <em> are a type of HTML5-based presentations that allow the user to create interactive and non-interactive content using a GUI web editor for dragging of titles, text content, option questions, open questions, multimedia and others </em>."

         paragraph ""

         paragraph "H5P is a popular and proven medium for active learning in contemporary education according to <strong> R. Singleton and A. Charlton, “Creating H5P content for active learning”, pjtel, vol. 2, no. 1, pp. 13-14, Nov. 2019. </strong>"

         new slide

         subtitle "Text components supported by H5PEL v0.1.0p"

         paragraph "Some of the allowed elements are:
               <ul>
                  <li> Titles </li>
                  <li> Subtitles </li>
                  <li> Paragraphs </li>
               </ul>
         "

         subtitle "Compatible HTML5 code"

         paragraph "The presentation elements in H5PEL are compatible with HTML tags such as strong, emphasized, unordered lists, and others."

      end

# Licensing

   H5PEL is published as a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 project. 
   See the **"LICENSE"** file for more information.

# Contact the author

Questions about code or the project can be asked by email at joseinestroza.developer at outlook dot com.

 -- [José Inestroza](https://github.com/joseinestroza/)