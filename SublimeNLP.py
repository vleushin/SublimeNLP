import sublime
import sublime_plugin
import collections
import operator
import re

class WordStatsCommand(sublime_plugin.TextCommand):
    def show_stats(self, stats):
        def stats_format(input):
            return '%d: %s' % (input[1], input[0])
        self.sorted_stats = sorted(stats.iteritems(), key=operator.itemgetter(1), reverse=True)
        items = map(stats_format, self.sorted_stats)
        self.view.window().show_quick_panel(items, None)

class FileWordStatsCommand(WordStatsCommand):
    def run(self, edit):
        terms = []
        self.view.find_all(r'\w+', sublime.IGNORECASE, '$0', terms)
        stats = collections.defaultdict(int)
        for term in terms:
            stats[term] += 1
        self.show_stats(stats)

class SelectionWordStatsCommand(WordStatsCommand):
    def run(self, edit):
        stats = collections.defaultdict(int)
        regions = [self.view.word(selection) if selection.empty() else selection for selection in self.view.sel()]
        for region in regions:
            for word in re.findall(r'\w+', self.view.substr(region), re.IGNORECASE):
                stats[word] += 1
        self.show_stats(stats)
