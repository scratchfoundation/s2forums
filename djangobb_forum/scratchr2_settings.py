import codecs

#DjangoBB Forum Settings
# Described here: https://bitbucket.org/slav0nic/djangobb/src/a4c0272533a9/djangobb_forum/settings.py
DJANGOBB_FORUM_BASE_TITLE = 'Discuss Scratch'
DJANGOBB_PM_SUPPORT = False
DJANGOBB_HEADER = 'Discuss Scratch'
DJANGOBB_TAGLINE = ''
DJANGOBB_REPUTATION_SUPPORT = False
DJANGOBB_ATTACHMENT_SUPPORT = False
DJANGOBB_GRAVATAR_SUPPORT = False
DJANGOBB_DISPLAY_PROFILE_MENU_OPTIONS = False
DJANGOBB_DISPLAY_AVATAR_OPTIONS = False
DJANGOBB_DISPLAY_USERTITLE = False
# The value is the topic id where deleted posts should be sent
DJANGOBB_SOFT_DELETE_POSTS = 412
# The value is the forum id where deleted topics should be sent
DJANGOBB_SOFT_DELETE_TOPICS = 2
DJANGOBB_ALLOW_POLLS = False
DJANGOBB_POST_FLOOD = True
DJANGOBB_POST_FLOOD_SLOW = 120
DJANGOBB_POST_FLOOD_MED = 60
DJANGOBB_TOPIC_CLOSE_DELAY = 24 * 60 * 60
DJANGOBB_POST_DELETE_DELAY = 24 * 60 * 60

# Spam settings
DJANGOBB_SPAM_CATEGORY_NAME = "Moderator Only Forums"
DJANGOBB_SPAM_FORUM_NAME = "Spam Dustbin"
DJANGOBB_SPAM_TOPIC_NAME = "Spam Dustbin"

DJANGOBB_TOPIC_PAGE_SIZE = 20
DJANGOBB_FORUM_PAGE_SIZE = 25
DJANGOBB_SIGNATURE_MAX_LINES = 10
DJANGOBB_SIGNATURE_MAX_LENGTH = 2000
DJANGOBB_AUTHORITY_SUPPORT = False
DJANGOBB_DEFAULT_TIME_ZONE = 0
DJANGOBB_IMAGE_HOST_WHITELIST = r'(?:(?:tinypic|photobucket|cubeupload)\.com|imageshack\.(?:com|us)|modshare\.tk|(?:scratchr|wikipedia|wikimedia|modshare\.futuresight)\.org|(?<!scratch\.mit)\.edu|scratch-dach\.info)$'

# Allowed paths for embedded images hosted on *.scratch.mit.edu
DJANGOBB_SCRATCH_IMAGE_PATH_WHITELIST = r'^(?:/scratchr2/static|/static/site/|/get_image/|/w/images/)'
#rot13 the filter for the sake of Scratchers linking to the public repo
DJANGOBB_LANGUAGE_FILTER = codecs.encode(r'(?v)\o(shtyl|(\j*?)shpx(\j*?)|s(h|i|\*)?p?x(vat?)?|(\j*?)fu(v|1|y)g(\j*?)|pe(n|@|\*)c(cre|crq|l)?|(onq|qhzo|wnpx)?(n|@)ff(u(b|0)yr|jvcr)?|(onq|qhzo|wnpx)?(n|@)efr(u(b|0)yr|jvcr)?|onfgneq|o(v|1|y|\*)?g?pu(r?f)?|phag|phz|(tbq?)?qnz(a|z)(vg)?|qbhpur(\j*?)|(arj)?snt(tbg|tng)?|sevt(tra|tva|tvat)?|bzst|cvff(\j*?)|cbea|encr|ergneq|frk|f r k|fung|fyhg|gvg|ju(b|0)er(\j*?)|jg(s|su|u))(f|rq)?\o', 'rot13')
