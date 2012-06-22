# Written by Barret Rennie, 2012
# This file is released into the public domain.

"""A markdown extension to allow gist inclusion in safe html mode."""

from markdown import Extension, Markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re

GIST_RE = r"{gist:([0-9a-f]+)}"
    
class GistPattern(Pattern):
    """Enable inclusion of gists into markdown.

    {gist:number} will include the appropriate gist.
    To escape a gist (i.e. to have "{gist:id}" as text), use \\{gist:id}.
    """
    def handleMatch(self, m):
        """Create a script tag which matches includes a javascript matching the
        gist id."""
        script = etree.Element("script")
        script.set("src", "https://gist.github.com/%s.js" % m.group(2))
        return script

class GistExtension(Extension):
    """The Gist extension for markdown."""
    def extendMarkdown(self, md, md_globals):
        """Add the inline pattern to the markdown patterns."""
        md.inlinePatterns.add("gist", GistPattern(GIST_RE), "_end")


def markdown(text):
    """Run markdown on text, including the gist extension."""
    md = Markdown(safe_mode="escape", extensions=[GistExtension()])

    return md.convert(text)
