from markdown import Extension, Markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re

GIST_RE = r"{gist:(\d+)}"
    
class GistPattern(Pattern):
    """Enable inclusion of gists into markdown.

    {gist:number} will include the appropriate gist.
    To escape a gist (i.e. to have "{gist:id}" as text), use \\{gist:id}.
    """
    def handleMatch(self, m):
        script = etree.Element("script")
        script.set("src", "http://gist.github.com/%s.js" % m.group(2))
        return script

class GistExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add("gist", GistPattern(GIST_RE), "_end")


def markdown(text):
    """Run markdown on text, including the gist extension."""
    md = Markdown(safe_mode="escape", extensions=[GistExtension()])

    return md.convert(text)
