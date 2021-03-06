#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest
import element.loaders
import element.node
import os

class YamlNodeLoaderTest(unittest.TestCase):
    def setUp(self):
        self.path = "%s/fixtures/data" % os.path.dirname(os.path.abspath(__file__))
        self.loader = element.loaders.YamlNodeLoader()

    def test_init(self):
        self.assertTrue(self.loader.supports("%s/2013/my-post-content.yml" % self.path))
        self.assertFalse(self.loader.supports("%s/2013/fake.yml" % self.path))

        node = self.loader.load("%s/2013/my-post-content.yml" % self.path)

        self.assertEquals("blog.post", node['type'])
        self.assertEquals("My Post Content", node['title'])

        self.assertIsNotNone(node['content'])

    def test_load_inline(self):
        node = self.loader.load("%s/2013/inline-content.yml" % self.path)

        self.assertTrue("content" in node)
        self.assertEquals(node["content"], "## my title\nLorem ipsum dolor sit amet, consectetur adipiscing elit.\n----\nyes try with double split ... which shouldn't split at this point")

class InlineLoaderTest(unittest.TestCase):

    def setUp(self):
        self.loader = element.loaders.InlineLoader()

    def test_support(self):
        self.assertFalse(self.loader.supports([]))
        self.assertFalse(self.loader.supports(''))
        self.assertFalse(self.loader.supports({}))
        self.assertFalse(self.loader.supports({'type': 'hello'}))

        self.assertTrue(self.loader.supports({'type': 'hello', 'id': 'salut'}))

    def test_load(self):
        node = self.loader.load({'type': 'hello', 'id': 'salut'})

        self.assertEquals('hello', node['type'])
        self.assertEquals('salut', node['id'])


