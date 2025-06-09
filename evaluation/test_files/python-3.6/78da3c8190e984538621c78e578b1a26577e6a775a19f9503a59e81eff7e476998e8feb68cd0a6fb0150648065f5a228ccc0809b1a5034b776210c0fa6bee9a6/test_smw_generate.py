"""
Created on 2023-01-18

@author: wf
"""
import os
from tests.basesmwtest import BaseSemanticMediawikiTest
from yprinciple.smw_targets import SMWTarget
from yprinciple.genapi import GeneratorAPI
from yprinciple.ypgen import YPGen
from yprinciple.ypcell import MwGenResult, FileGenResult

class TestSMWGenerate(BaseSemanticMediawikiTest):
    """
    test Semantic MediaWiki handling
    """

    def setUp(self, debug=False, profile=True):
        BaseSemanticMediawikiTest.setUp(self, debug=debug, profile=profile)
        for wikiId in ['cr']:
            self.getWikiUser(wikiId, save=True)

    def getMarkup(self, debug: bool=False, wikiId='cr', context_name='CrSchema', topicNames=['Event'], target_keys=['category', 'concept', 'form', 'help', 'listOf', 'template']):
        """
        get the markups for a given context, topicNames and target keys
        """
        (_smwAccess, context) = self.getContext(wikiId, context_name, debug)
        for topicname in topicNames:
            topic = context.topics[topicname]
            for target_key in target_keys:
                smwTarget = SMWTarget.getSMWTargets()[target_key]
                markup = smwTarget.generate(topic)
                yield (topicname, target_key, smwTarget, markup)

    def test_Issue13_ExternalIdentifer_Link_handling(self):
        """
        show Links for external Identifiers in templates
        https://github.com/WolfgangFahl/py-yprinciple-gen/issues/13
        """
        debug = self.debug
        for (_topicname, _target_key, _smwTarget, markup) in self.getMarkup(debug, target_keys=['template']):
            if debug:
                print(markup)
            self.assertTrue('{{#show: {{FULLPAGENAME}}|?Event wikidataid}}' in markup)

    def test_Issue12_TopicLink_handling(self):
        """
        test Topic link handling
        """
        debug = self.debug
        for (_topicname, _target_key, _smwTarget, markup) in self.getMarkup(target_keys=['form'], debug=debug):
            if debug:
                print(markup)
            expected = '{{{field|city|property=Event city|input type=dropdown|values from concept=City}}}'
            self.assertTrue(expected in markup)

    def test_Issue28_viewmode_masterdetail(self):
        """
        test master/detail viewmode generation and TopicLink separator
        
        https://github.com/WolfgangFahl/py-yprinciple-gen/issues/28
        refactor viewmode "masterdetail"
        
        """
        debug = self.debug
        for (_topicname, target_key, _smwTarget, markup) in self.getMarkup(wikiId='wiki', context_name='MetaModel', topicNames=['Context'], target_keys=['template'], debug=debug):
            if target_key == 'template':
                if debug:
                    print(markup)
                expected_parts = ['= topics =', '{{#ask:[[Concept:Topic]][[Topic context::{{FULLPAGENAME}}]]']
                for expected in expected_parts:
                    self.assertTrue(expected in markup)

    def test_Issue29_TopicLink_separator(self):
        """
        https://github.com/WolfgangFahl/py-yprinciple-gen/issues/29
        1:N relation using TopicLink separator
    
        """
        debug = self.debug
        for (_topicname, target_key, _smwTarget, markup) in self.getMarkup(topicNames=['Paper'], target_keys=['template'], debug=debug):
            if target_key == 'template':
                if debug:
                    print(markup)
                expected_parts = ['|Paper authors={{{authors|}}}|+sep=,', '{{!}}&nbsp;{{#if:{{{authors|}}}|{{{authors}}}|}}→{{#show: {{FULLPAGENAME}}|?Paper authors}}']
                for expected in expected_parts:
                    self.assertTrue(expected in markup)

    def test_genbatch(self):
        """
        test the batch generator
        """
        parser = YPGen.getArgParser('YPGen automation test', 'No specific version - just testing')
        argv = ['--wikiId', 'cr', '--context', 'CrSchema', '--topics', 'Event', '--targets', 'help']
        args = parser.parse_args(argv)
        gen = GeneratorAPI.fromArgs(args)
        self.assertIsNone(gen.error)
        self.assertIsNone(gen.errMsg)
        if not self.inPublicCI():
            genResults = gen.generateViaMwApi(args.targets, args.topics, dryRun=not args.noDry)
            self.assertTrue(len(genResults) == 1)
            genResult = genResults[0]
            self.assertTrue(isinstance(genResult, MwGenResult))
        genResults = gen.generateToFile(target_dir='/tmp/ypgentest', target_names=args.targets, topic_names=args.topics, dryRun=False)
        self.assertTrue(len(genResults) == 1)
        genResult = genResults[0]
        self.assertTrue(isinstance(genResult, FileGenResult))
        self.assertTrue('Help:Event.wiki' in genResult.path)
        self.assertTrue(os.path.isfile(genResult.path))