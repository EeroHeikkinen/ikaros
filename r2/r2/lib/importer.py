from gdata import atom

import sys
import os

# from r2.models import Link,Comment,Account,Subreddit

###########################
# Constants
###########################

#BLOGGER_URL = 'http://www.blogger.com/'
#BLOGGER_NS = 'http://www.blogger.com/atom/ns#'
KIND_SCHEME = 'http://schemas.google.com/g/2005#kind'

#YOUTUBE_RE = re.compile('http://www.youtube.com/v/([^&]+)&?.*')
#YOUTUBE_FMT = r'[youtube=http://www.youtube.com/watch?v=\1]'
#GOOGLEVIDEO_RE = re.compile('(http://video.google.com/googleplayer.swf.*)')
#GOOGLEVIDEO_FMT = r'[googlevideo=\1]'
#DAILYMOTION_RE = re.compile('http://www.dailymotion.com/swf/(.*)')
#DAILYMOTION_FMT = r'[dailymotion id=\1]'

class AtomImporter(object):

    def __init__(self, doc):
        """Constructs an importer for an Atom (Blogger export) file.

        Args:
        doc: The Atom file as a string
        """

        # Ensure UTF8 chars get through correctly by ensuring we have a
        # compliant UTF8 input doc.
        self.doc = doc.decode('utf-8', 'replace').encode('utf-8')

        # Read the incoming document as a GData Atom feed.
        self.feed = atom.FeedFromString(self.doc)

    def show_posts_by(self, authors):
        """Print the titles of the posts by the list of supplied authors"""
        
        for entry in self.feed.entry:
            # Grab the information about the entry kind
            entry_kind = ""
            for category in entry.category:
              if category.scheme == KIND_SCHEME:
                entry_kind = category.term

            if entry_kind.endswith("#comment"):
              # # This entry will be a comment, grab the post that it goes to
              # in_reply_to = entry.FindExtensions('in-reply-to')
              # post_item = None
              # # Check to see that the comment has a corresponding post entry
              # if in_reply_to:
              #   post_id = self._ParsePostId(in_reply_to[0].attributes['ref'])
              #   post_item = posts_map.get(post_id, None)
              # 
              # # Found the post for the comment, add the commment to it
              # if post_item:
              #   # The author email may not be included in the file
              #   author_email = ''
              #   if entry.author[0].email:
              #     author_email = entry.author[0].email.text
              # 
              #   # Same for the the author's url
              #   author_url = ''
              #   if entry.author[0].uri:
              #     author_url = entry.author[0].uri.text
              # 
              #   post_item.comments.append(wordpress.Comment(
              #       comment_id = self._GetNextId(),
              #       author = entry.author[0].name.text,
              #       author_email = author_email,
              #       author_url = author_url,
              #       date = self._ConvertDate(entry.published.text),
              #       content = self._ConvertContent(entry.content.text)))
              # 
              pass
            elif entry_kind.endswith("#post"):
              # This entry will be a post
              for author in entry.author:
                  if author.name.text in authors:
                      print '%s by %s' % (entry.title.text, author.name.text)
                      break
            
              # post_item = self._ConvertPostEntry(entry)
              # posts_map[self._ParsePostId(entry.id.text)] = post_item
              # wxr.channel.items.append(post_item)

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print 'Usage: %s <blogger_export_file>' % os.path.basename(sys.argv[0])
    print
    print ' Imports the blogger export file.'
    sys.exit(-1)

  xml_file = open(sys.argv[1])
  xml_doc = xml_file.read()
  importer = AtomImporter(xml_doc)
  print importer.show_posts_by('Eliezer Yudkowsky')
  xml_file.close()