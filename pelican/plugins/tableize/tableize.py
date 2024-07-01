#
# HTML re-formatting of <table>/<tbody>/<td>/<tr>
#
# The defaults are:
#    Auto Index is disabled
#    Separator symbol is a pipe ("|")
#    Table header is disabled
#    Default HTML template is used as:
#        <div class="tableize">
#        <table class="tableize">
#          {%- if caption %}
#          <caption> {{ caption }} </caption>
#          {%- endif %}
#          {%- if th != 0 %}
#          <thead class="tableize">
#          <tr class="tableize">
#            {%- if ai == 1 %}
#            <th class="tableize"> No. </th>
#            {%- endif %}
#            {%- for head in heads %}
#            <th class="tableize">{{ head }}</th>
#            {%- endfor %}
#          </tr>
#          </thead>
#          {%- endif %}
#          <tbody class="tableize">
#            {%- for body in bodies %}
#            <tr class="tableize">
#              {%- if ai == 1 %}
#              <td class="tableize">{{ loop.index }}  </td>
#              [%- endif %}
#              {%- for entry in body %}
#              <td class="tableize">{{ entry }}</td>
#              {%- endif %}
#            </tr>
#          </tbody>
#        </table>
#        </div>
#
#  To change the default of HTML re-formatting of <table>, et. al., for an entire
#  Pelican project, use 'TABLEIZE_PLUGIN' as a dict type in the following snippet
#  example used in its `pelicanconf.py` configuration file used in your Pelican project.
#
#      TABLEIZE_PLUGIN = {
#          'ai': 1,
#          'separator': ',',
#          'th': True
#          'template': """
#              <div>
#                <table class="tableize">
#                   ...
#                </table>
#              </div>
#              ...
#          """
#          }
#
#
#
from copy import copy
import pprint
import logging
from pelican import signals, logger
from pelican.readers import BaseReader
from pelican.contents import Article, Page
from pelican.settings import DEFAULT_CONFIG

logger = logging.getLogger('added2ndname')  # log with my plugin name
logger = logging.getLogger(__name__)  # log with my plugin name

# What to expect in finding inside the Pelican
# `pelicanconf.py`/`publishconf.py`) configuration setting file
#
#    TABLEIZE_PLUGIN = {}
#

# Configuration variable name and its dictionary keywords
PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME = 'TABLEIZE_PLUGIN'
PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_AI = 'ai'
PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_TH = 'th'
PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_SEPARATOR = 'separator'
PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_TEMPLATE = 'template'

#

DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_SEPARATOR = '|'
DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_AUTO_INDEX = 1
DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TABLE_HEADER = False
DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TEMPLATE = """
<div class="tableize">
  <table class="tableize">
    {%- if caption %}
    <caption> {{ caption }} </caption>
    {%- endif %}
    {%- if th != 0 %}
    <thead class="tableize">
    <tr class="tableize">
      {%- if ai == 1 %}
      <th class="tableize"> No. </th>
      {%- endif %}
      {%- for head in heads %}
      <th class="tableize">{{ head }}</th>
      {%- endfor %}
    </tr>
    </thead>
    {%- endif %}
    <tbody class="tableize">
      {%- for body in bodies %}
      <tr class="tableize">
        {%- if ai == 1 %}
        <td class="tableize">{{ loop.index }}  </td>
        [%- endif %}
        {%- for entry in body %}
        <td class="tableize">{{ entry }}</td>
        {%- endif %}
      </tr>
    </tbody>
  </table>
</div>"""

# Shouldn't we be putting global variables into reader.settings (aka Pelican config)?
pp_tableize_initialized = False  # NOQA  # those value disappears at next call?
pp_tableize_sanity_found = False  # NOQA  # those value disappears at next call?


def set_default_settings(settings):
    """ If the pelican.settings is missing any of our plugin settings,
        fill those settings as well."""
    settings.setdefault(
        PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME,
        {
            PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_AI:
                DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_AUTO_INDEX,
            PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_TH:
                DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TABLE_HEADER,
            PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_SEPARATOR:
                DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_SEPARATOR,
            PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_KEYWORD_TEMPLATE:
                DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TEMPLATE
        }
    )


def check_plugin_settings(pelican):
    if pelican is None:
        return
    tbp_settings = copy(pelican.settings[PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME])
    set_default_settings(DEFAULT_CONFIG)
    for key in tbp_settings:
        warning_text = 'Tableize plugin -> "%s" must be ' % key
        typeof_def_value = type(DEFAULT_CONFIG[PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME][key])
        types = {
            str: "a string.",
            int: "an integer.",
            bool: "a boolean."
        }
        if type(tbp_settings[key]) != typeof_def_value:
            logging.warning(warning_text + types[typeof_def_value])
            continue
    pelican.settings['ACE_EDITOR_PLUGIN'] = copy(
        DEFAULT_CONFIG['ACE_EDITOR_PLUGIN']
    )
    set_default_settings(pelican.settings)


# Create a new reader class, inheriting from the pelican.reader.BaseReader
class NewReader(BaseReader):
    enabled = True  # Yeah, you probably want that :-)

    # The list of file extensions you want this reader to match with.
    # If multiple readers were to use the same extension, the latest will
    # win (so the one you're defining here, most probably).
    file_extensions = ['yeah']

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        metadata = {'title': 'Oh yeah',
                    'category': 'Foo',
                    'date': '2012-12-01'}

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        return "Some content", parsed


def tableize_pelican_find_smarty(ppt_pelican):
    global pp_tableize_sanity_found
    global pp_tableize_initialized

    # See if MARKDOWN item is in the Pelican configuration settings
    if 'MARKDOWN' in ppt_pelican.settings.keys():
        logger.debug('MARKDOWN is in pelican.settings;')
        # check that MARKDOWN is a [] dict type
        if isinstance(ppt_pelican.settings['MARKDOWN'], dict):
            # get the settings of Markdown "plugin"
            pp_markdown_settings = ppt_pelican.settings['MARKDOWN']
            logger.debug('MARKDOWN is a dict type')
            # check for existence of 'extension_configs' item in MARKDOWN[] dict
            if 'extension_configs' in pp_markdown_settings.keys():
                logger.debug('extension_configs item found in MARKDOWN dict')
                pp_markdown_exts_configs = pp_markdown_settings['extension_configs']
                if 'markdown.extensions.smarty' in pp_markdown_exts_configs.keys():
                    logger.info('markdown.extensions.smarty is found in ' +
                                'MARKDOWN[\'extension_configs\'] dict')
                    # Compensate for other processor replacing single/double quote
                    # symbols with &rdquo
                    pp_tableize_sanity_found = True
                else:
                    logger.info('markdown.extensions.smarty is NOT found in ' +
                                'MARKDOWN[\'extension_config\'] dict; Check config ' +
                                'file; tableize plugin is disabled')
                    pp_tableize_sanity_found = False
                return
            else:
                logger.debug(
                    '\'extension_configs\' not in MARKDOWN dict; Check config file;' +
                    'tableize plugin is disabled')
                pp_tableize_sanity_found = False
        else:
            logger.debug(
                'MARKDOWN dict does not exist; Check config file;' +
                'tableize plugin is disabled')
            pp_tableize_sanity_found = False
    else:
        pp_tableize_sanity_found = False

    pp_tableize_initialized = True


def tableize_pelican_initialized_all(pelican):
    # arg1 : pelican:Pelican object
    #
    # pelican:Pelican object provides the following variable member items:
    #   delete_outputdir:bool, ignore_files:list, output_path:str,
    #     output_retention:list, path:str, plugins:list, settings:dict,
    #     and theme:str.
    #
    # Hooked by signals.initialized.connect().
    #
    tpp_pelican = pelican  # NOQA
    if tpp_pelican is None:
        logger.fatal('No pelican access; tableize plugin is disabled')
        return

    # Scan for "Sanity" plugin which are capable of replacing the single/double
    # quote symbols with `&rdquo`, we have to watch out for those
    logger.debug("tableize_pelican_initialized_all signal")
    if not isinstance(tpp_pelican, object):
        logger.fatal('pelican is not an object type; tableize plugin is disabled')
        return

    if tpp_pelican.__class__.__bases__.__contains__('settings'):
        logger.critical(
            '\'pelican.settings\' does not exist tableize plugin is disabled')
        return

    if not isinstance(tpp_pelican.settings, dict):  # NOQA
        logger.critical(
            'pelican.settings is not a dict type; tableize plugin is disabled')
        return

    plugin_logger = logging.getLogger(__name__)
    tpp_pelican_settings = tpp_pelican.settings  # NOQA
    # Check the MARKDOWN "plugin" to see if they got features that runs
    # counterproductive to this plugin's effort of dealing with single/double quotes

    tableize_settings = pelican.settings.get(PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME)
    if tableize_settings is None:
        logger.warning('%s does not exist in pelican.settings; ' +
                       'plugin\'s built-in defaults used',
                       PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME)
        # this is the part where we must implicitly declare our defaults
        set_default_settings(pelican.settings)
    else:
        # explicit settings for this plugin are found in
        #     pelican.settings['TABLEIZE_PLUGIN']
        logger.debug('{0!s} exists in pelican.settings'.format(
            PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME))
        tableize_settings = copy(
            tpp_pelican_settings[PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME])
        check_plugin_settings(tpp_pelican)
    # This plugin settings is never in pelican's DEFAULT_CONFIG, so we skip that
    # Any explicit plugin setting is found ONLY in `pelican.settings`

    tableize_pelican_find_smarty(tpp_pelican)

    tpp_pelican.settings.setdefault('TABLEIZE_AUTO_INDEX',
                                    DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_AUTO_INDEX)
    tpp_pelican.settings.setdefault('TABLEIZE_TABLE_HEADER',
                                    DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TABLE_HEADER)
    tpp_pelican.settings.setdefault('TABLEIZE_SEPARATOR',
                                    DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_SEPARATOR)
    tpp_pelican.settings.setdefault('TABLEIZE_TEMPLATE',
                                    DEFAULT_TABLEIZE_PLUGIN_PELICAN_CONFIG_TEMPLATE)

    # save back into pelican.settings
    pelican.settings[PELICAN_CONFIG_PLUGIN_TABLEIZE_ITEM_NAME] = \
        tableize_settings
    # tableize_settings is going to disappear when we leave this function
    # store it back into pelican.settings? or leave as plugin's global object?

    logger.debug('tableize pelican plugin initialized')


def tp_article_init(articles_generator):
    # arg1 : articles_generator:ArticlesGenerator
    #
    # articles_generator provides the following variable member items:
    #   articles:list, authors:dict, categories:dict, context:dict, dates:dict,
    #   drafts:list, drafts_translation:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives_dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   translations:list.
    #
    # 1st article-related signal.
    # generator processing Class (i.e., ArticlesGenerator, PagesGenerator,
    #     StaticGenerator).
    # no content, no articles, but lots of other stuffs.
    # first appearance of article_generator.settings.
    # Callstack:
    #     ArticlesGenerator.__init__()
    #
    #
    # Hooked by signals.article_generator_init.connect()
    logger.info('tp_article_init called: path is ' + articles_generator.path)
    return


def tp_article_preread(articles_generator):
    # Description:
    #     useful for modifying file-related variables before reading
    #     this is the only article-related signal BEFORE any Markdown pre-processing
    #
    # arg1 : articles_generator:ArticlesGenerator
    #
    # articles_generator:Articles_generator provides the following
    # variable member items:
    #   articles:list, authors:dict, categories:dict, context:dict, dates:dict,
    #   drafts:list, drafts_translations:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives:dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   and translations:list.  (No content here, yet)
    #
    # 2nd article-related signal
    # First signal for entire ArticleGenerator.generate_context()
    # First signal within Readers.read_file().
    # Callstack:
    #                 signals.article_generator_preread.send()
    #                 ArticlesGenerator.generate_context()
    #                 Pelican.run()
    #
    # Hooked by signals.article_generator_preread.connect().
    #
    print('tp_article_preread called')
    return


def tp_article_context(articles_generator, metadata=[]):
    # Description:
    #     context and metadata are added here the first time for
    #     ArticlesGenerator but still no content yet.
    #
    # arg1 : articles_generator:ArticlesGenerator
    # arg2 : metadata:dict
    #
    # articles_generator of ArticlesGenerator class provides the
    # following variable member items:
    #   articles:list, authors:dict, categories:dict, context:dict,
    #   dates:dict, drafts:list,
    #   drafts_translations:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives:dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   and translations:list.  (No content here, yet)
    #
    # metadata of dict type provides the following variable member items:
    #   status:str, category:Category, reader:str, title:str, data:SafeDatetime,
    #   tags:list, summary:str, lang:str, private:str, and __len__:int.
    #
    # 3rd article-related signal.
    # 2nd signal for entire ArticleGenerator.generate_context().
    # 1st param is Generator type (ArticlesGenerator/PagesGenerator/StaticGenerator).
    # 2nd param is metadata dict object (what you see in first few lines of an
    #     article/page/static file).
    #
    # Hooked by signals.article_generator_context.connect().
    #
    print('tp_article_context called')
    return


def tp_content_object_init(content_class: object):
    # Description:
    #   First signal handler to provide the actual content of any article/page/static
    #   file.
    #
    # arg1 : content_class:Content, could be article:Article, page:Page, static:Static
    #
    # article of Article(Content) subclass provides the following variable member items:
    #   allowed_statuses:tuple, author:Author, authors:list, category:Category,
    #   content:str, date:SafeDatetime, date_format:str, default_status:str,
    #   default_template:str, filename:str, get_content:partial, get_summary:partial,
    #   in_default_lang:bool, lang:str, locale_date:str, mandatory_properties:tuple,
    #   metadata:dict, private:str, reader:str, relative_dir:str,
    #   relative_source_path:str, save_as:str, settings:dict, slug:str,
    #   source_path:str, status:str, summary:str, tags:list, template:str,
    #   timezone:Zoneinfo, title:str, translations:list, url:str, url_format:dict
    #
    # Callstack:
    #     signals.content_object_init.send()
    #     Content.__init__()
    #     Article.__init__()
    #     Readers.read_file()
    #     ArticlesGenerator.generate_context()
    #     Pelican.run()
    #
    # 4th article-related signal.
    # 3rd signal in ArticlesGenerator.generate_context().
    # Still inside read_file().
    # First signal appearance having a content provided by Markdown.read_file().
    #
    # Hooked using signals.content_object_init.connect(tp_content_object_init).
    #
    print('tp_content_object_init called')
    if content_class is None:
        return
    content = content_class.content

    print('tp_content_object_init: content: {0!s}'.format(content))

    # Only process Article or Page subclass contents
    if not (isinstance(content_class, Article) or isinstance(content_class, Page)):
        return

    return


def tp_article_pretaxonomy(articles_generator):
    # Description:
    #   Now you can first tell if it came from ArticlesGenerator or StaticGenerator
    #      using self variable.
    #   But the content is now gone.
    #   After all translations are done, after a complete list of all document file
    #       is made for each generator type.
    #   All about indexing, cross-linking and translation, plugins who want the
    #   metadata after such translation/index/lists updating;
    #   absolutely no content (anymore).
    #
    # arg1: articles_generator:ArticlesGenerator
    #
    # articles_generator of ArticlesGenerator class provides the
    # following variable member items:
    #   articles:list, authors:dict, categories:dict, content:dict,
    #   dates:dict, drafts:list,
    #   drafts_translations:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives:dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   and translations:list.
    #
    # 5th article-related signal.
    # 4th signal in ArticlesGenerator.generate_context().
    #
    # Hooked by signals.article_generator_pretaxonomy.connect(tp_article_pretaxonomy).
    #
    print('tp_article_pretaxonomy called')
    return


def tp_article_finalized(articles_generator):
    # Description:
    #
    # arg1 : articles_generators:ArticlesGenerator
    #
    # articles_generator of ArticlesGenerator class provides the
    # following variable member items:
    #   articles:list, authors:dict, categories:dict, context:dict
    #   dates:dict, drafts:list,
    #   drafts_translations:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives:dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   and translations:list.
    #
    # 5th article-related signal.
    # The last signal in ArticlesGenerator.generate_context().
    # all the caches are saved.
    #
    # Hooked by signals.article_generator_finalized.connect(tp_article_finalized).
    #
    print('tp_article_finalized called')
    return


def tp_article_write(articles_generator, content=[]):
    #
    # arg1 : articles_generator:ArticlesGenerator
    # arg2 : content:Article
    #
    # articles_generator of ArticlesGenerator class provides the
    # following variable member items:
    #   articles:list, authors:dict, categories:dict, context:dict
    #   dates:dict, drafts:list,
    #   drafts_translations:list, env:Environment, hidden_articles:list,
    #   hidden_translations:list, output_path:str, path:str, period_archives:dict,
    #   readers:Readers, related_posts:list, settings:dict, tags:dict, theme:str,
    #   and translations:list.
    #
    # content of Article class provides the following variable member items:
    #   allowed_statuses:tuple, author:Author, authors:list, category:Category,
    #   content:str, date:SafeDatetime, date_format:str, default_status:str,
    #   default_template:str, filename:str, get_content:partial, get_summary:partial,
    #   in_default_lang:bool, lang:str, locale_date:str, mandatory_properties:tuple,
    #   metadata:dict, private:str, reader:str, relative_dir:str,
    #   relative_source_path:str, save_as:str, settings:dict, slug:str,
    #   source_path:str, status:str, summary:str, tags:list, template:str,
    #   timezone:Zoneinfo, title:str, translations:list, url:str, url_format:dict
    #
    # 6th article-related signal.
    # 5th signal in ArticlesGenerator.generate_context().
    # Article.content is back.
    # Article.metadata is back.
    #
    # Hooked by signals.article_generator_write_article.connect(tp_article_write).
    #
    print('tp_article_write called')
    return


# This is how pelican plugin works.
# register() is a well-established function name used by Pelican plugin
# handler for this plugin to get recognized, inserted, initialized, and
# its processors added into and by the Pelican app.
def register():

    signals.initialized.connect(tableize_pelican_initialized_all)

    # Different version of Pelican behave differently.
    # By using 'try', we ensure that all signals are available before
    # our plugin processing.
    try:
        # All signals are listed here as of Pelican v4.9.1
        # signals.get_generators.connect()
        # signals.readers_init()
        # signals.generator_init()
        signals.article_generator_init.connect(tp_article_init)
        # signals.readers_init()
        # signals.readers_init()
        # signals.generator_init()
        # signals.page_generator_init()
        # signals.readers_init()
        # signals.generator_init()
        # signals.readers_init()
        # signals.generator_init()
        # signals.static_generator_init()
        signals.article_generator_preread.connect(tp_article_preread)
        signals.article_generator_context.connect(tp_article_context)
        signals.content_object_init.connect(tp_content_object_init)
        signals.article_generator_pretaxonomy.connect(tp_article_pretaxonomy)
        signals.article_generator_finalized.connect(tp_article_finalized)
        # signals.page_generator_preread.connect(tp_page_preread)
        # signals.page_generator_context.connect(tp_page_context)
        # signals.content_object_init.connect(tp_content_object_init)
        # signals.page_generator_finalized.connect(tp_page_finalized)
        # signals.static_generator_preread.connect(tp_static_preread)
        # signals.static_generator_context.connect(tp_static_context)
        # signals.content_object_init.connect(tp_content_object_init)
        # signals.static_generator_finalized.connect(tp_static_finalized)
        # signals.all_generators_finalized.connect(tp_all_generators_finalized)
        # signals.get_writers()
        # signals.feed_generated()
        # signals.feed_written()
        signals.article_generator_write_article.connect(tp_article_write)
        # signals.content_written()
        # signals.article_writer_finalized.connect(tp_article_write)
        # signals.page_generator_write_page.connect(tp_article_write)
        # signals.content_written()
        # signals.page_writer_finalized()
        # signals.content_written()
        # signals.pelican_finalized()
    except Exception as e:
        logger.exception('Plugin failed to execute: {}'.format(pprint.pformat(e)))

    logger.info(
        'tableize plugin registered for Pelican, using new 4.0 plugin variant')
