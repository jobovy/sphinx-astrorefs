# pybtex_astro.py: Astro labeling and reference formatting
import re
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.formatting import toplevel
from pybtex.style.labels import BaseLabelStyle
from pybtex.style.sorting.author_year_title \
    import SortingStyle as AuthorSortingStyle
from pybtex.richtext import Symbol, Text
from pybtex.plugin import register_plugin
from pybtex.style.template import (
    field, first_of, href, join, names, optional, optional_field, sentence,
    tag, together, words, node, FieldIsMissing
)
import latexcodec
from sphinx.util import logging
logger= logging.getLogger(__name__)

def decode_specialchars(input):
    return input.replace('{', '').replace('}', '').encode().decode('latex')

# labels in astro format: author year, author & author year for two authors
# author et al. year for more than two
class AstroLabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        for entry in sorted_entries:
            if len(entry.persons['author']) == 1:
                out= '{} {}'.format(entry.persons['author'][0].last_names[0],
                                    entry.fields['year'])
            elif len(entry.persons['author']) == 2:
                out= '{} & {} {}'.format(entry.persons['author'][0]\
                                             .last_names[0],
                                         entry.persons['author'][1]\
                                              .last_names[0],
                                         entry.fields['year'])
            else:
                out= '{} et al. {}'.format(entry.persons['author'][0]\
                                               .last_names[0],
                                          entry.fields['year'])
            yield decode_specialchars(out)

def dashify(text):
    dash_re = re.compile(r'-+')
    return Text(Symbol('ndash')).join(text.split(dash_re))

def format_first_and_last_name(person):
    if len(person.first_names) > 0:
        return '{} {}.'.format(decode_specialchars(person.last_names[0]),
                               str(person.first_names[0])[0])
    else: # collaboration or similar
        return '{}'.format(decode_specialchars(person.last_names[0]))

@node
def astro_names(children, context, role, **kwargs):
    """Return formatted names."""
    assert not children
    try:
        persons= context['entry'].persons[role]
    except KeyError:
        raise FieldIsMissing(role, context['entry'])
    if len(persons) > 5:
        out= ''
        for ii in range(5):
            out+= '{}, '.format(format_first_and_last_name(persons[ii]))
        return '{}et al.'.format(out)
    elif len(persons) > 2:
        out= ''
        for ii in range(len(persons)-1):
            out+= '{}, '.format(format_first_and_last_name(persons[ii]))
        return '{}& {}'.format(out,
                                format_first_and_last_name(persons[-1]))
    elif len(persons) == 2:
        return '{} & {}'.format(format_first_and_last_name(persons[0]),
                                format_first_and_last_name(persons[1]))
    else:
        return format_first_and_last_name(persons[0])

class AstroStyle(UnsrtStyle):
    default_label_style = AstroLabelStyle
    default_sorting_style= AuthorSortingStyle

    def format_names(self, role, as_sentence=True):
        formatted_names= astro_names(role,sep=', ',
                                     sep2 = ' & ',last_sep=', & ')
        if as_sentence:
            return sentence [formatted_names]
        else:
            return formatted_names

    def format_author(self,e,as_sentence=True):
        authors= self.format_names('author', as_sentence=False)
        return sentence[authors]

    def format_journal(self,e):
        if 'doi' not in e.fields:
            return field('journal')
        else:
            return href [
                join [
                    'https://doi.org/',
                    field('doi', raw=True)
                    ],
                field('journal')
                ]

    def format_volume(self,e):
        if 'adsurl' not in e.fields:
            return field('volume')
        else:
            return href [ field('adsurl',raw=True),
                          field('volume')]

    def format_pages(self,e):
        if 'eprint' not in e.fields:
            return field('pages',apply_func=dashify)
        else:
            return href [
                join [
                    'https://arxiv.org/abs/',
                    field('eprint', raw=True)
                    ],
                field('pages',apply_func=dashify)
                ]

    def get_article_template(self, e):
        journal_and_volume = join [
            tag('em') [self.format_journal(e)],' ',
            tag('strong') [self.format_volume(e)]
            ]
        template = toplevel [
            self.format_author(e),
            self.format_title(e, 'title'),
            sentence [
                journal_and_volume,
                join [
                    optional [self.format_pages(e)],
                    ' (',field('year'),')']
                ]
        ]
        return template

    def get_book_template(self, e):
        template = toplevel [
            self.format_author_or_editor(e),
            self.format_btitle(e, 'title'),
            self.format_volume_and_series(e),
            sentence [
                join [
                    field('publisher'),
                    optional [', ',field('address')],
                    ' (',field('year'),')']
                ],
            optional[ sentence [ self.format_isbn(e) ] ],
            self.format_web_refs(e),
        ]
        return template

def register():
    logger.info("Registering astro-style pybtex formatting...")
    register_plugin('pybtex.style.formatting', 'astrostyle', AstroStyle)
