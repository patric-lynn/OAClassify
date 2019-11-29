# -*- coding: utf-8 -*-
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WikiSpiderPipeline(object):
    def process_item(self, item, spider):
        class_name = item['class_name']
        topic = item['topic']
        facets = item['facets']
        output_path = '../../../../output/A_generate_all_entities/' + class_name
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        with open(output_path + '/' + topic + '.txt', 'w', encoding='utf-8') as f:
            wfacets = [f + '\n' for f in facets]
            f.writelines(wfacets)
        return 'Done: ' + topic
