from abc import ABC

from src.metrics.node_metrics import NodeMetrics
from src.model.node.node import Node
from src.util.logger import get_logger

logger = get_logger(__name__)


class Analyzer(ABC):
    def __init__(self, driver, options):
        self.driver = driver
        self.options = options
        self.xpath_patterns = ["//button", "//a", "//input", "//option", "//textarea"]

    # Node의 정보를 JavaScript 를 이용하여 속성이 담긴 list를 생성합니다.
    def collect_js(self):
        """
        collects actionable elements

        :return: a list of actionable elements
        """
        xpath_str = " ".join(self.xpath_patterns)

        script = """
            var Node = function(tag, type, rect, label, xpath, href, target) {
                this.tag = tag;
                this.type = type;
                this.rect = rect;
                this.label = label;
                this.xpath = xpath;
                this.href = href;
                this.target = target;
                return this;
            }

            function findElementsByXpath(pattern, contextNode) {
                if(contextNode === undefined) {
                  var xpathResult = document.evaluate(pattern, document, null, XPathResult.ANY_TYPE, null);
                } else {
                  var xpathResult = document.evaluate(pattern, contextNode, null, XPathResult.ANY_TYPE, null);
                }
                var array = [];
                var element = xpathResult.iterateNext();
                while(element) {
                  array.push(element);
                  element = xpathResult.iterateNext();
                }
                return array;
            }

            function collect(xpath) {
              var collected = [];
              patterns = xpath.split(" ");
              for (var pattern of patterns) {
                  elements = findElementsByXpath(pattern, document);
                  if (elements) {
                      collected = collected.concat(elements);
                  }
              }
              return collected;  
            }

            function isEnabled(element) {
                if (element.tagName === \"A\") {
                    return element.hasAttribute(\"href\");
                } else if (element.tagName === \"INPUT\") {
                    if (!element.hasAttribute(\"type\")) return false;
                    if (element.getAttribute(\"type\") === \"hidden\") return false;
                    if (element.hasAttribute(\"style\") &&
                        element.getAttribute(\"style\") != \"style:none\") {
                        return false;
                    }
                } else if (element.hasAttribute(\"disabled\")) {
                    return !element.getAttribute(\"disabled\");
                }
                return true;
            }
            
            function createNodes(elements) {
                var nodes = [];
                for (element of elements) {
                    if (element && isEnabled(element)) {
                      let tagName = element.tagName;
                      let rect = element.getBoundingClientRect()
                      let label = findLabel(element);
                      if (tagName === \"A\") {
                        label = findLinkLabel(element);
                      }
                      let xpath = getRelativeXpath(element);
                      let type = element.getAttribute(\"type\");
                      let href = element.getAttribute(\"href\");
                      let target = element.getAttribute(\"target\");
                      let node = new Node(tagName.toLowerCase(), type, rect, label, xpath, href, target);
                      nodes.push(node);
                    }
                }
                return nodes;
            }
            
            function getRelativeXpath(element) {
              if (element) {
                  var parents = findElementsByXpath(\"./ancestor::*\", element);
                  var size = parents.length;
            
                  let path = \"\";
                  var current = element;
            
                  for (var i = size - 1; i > -1; i--) {
                      var tag = current.tagName.toLowerCase();
                      // NB: comment/uncomment below to make the xpath relative or absolute anchored by an id
                      var element_id = current.getAttribute(\"id\");
                      if (element_id) {
                          var tag_id = `//*[@id=\'${element_id}\']`;
                          return tag_id + path;
                      }
            
                      var siblings = findElementsByXpath(\"./preceding-sibling::\" + tag, current);
                      var level = siblings.length + 1;
                      path = `/${tag}[${level}]${path}`;
                      current = findElementByXpath(\"./parent::*\", current);
                  }
                  return \"/\" + current.tagName.toLowerCase() + path;
              } else {
                  return null;
              }
            }
            
            function findLinkLabel(element) {
                let label = element.innerText;
                if (!label) {
                    label = findLabel(element);
                }
                
                if (!label) {
                    label = element.getAttribute(\"href\");
                }
                
                if (label) {
                    label = label.replace(/\\s{2,}/gi, ' ').replace(/['\"]+/g, '').replace(/\\n/g, ' ');
                } 
                return label;   
            }
            
            function findLabel(element) {
                let label = element.innerText;
                if (!label) {
                    label = element.getAttribute(\"name\");
                }
                if (!label) {
                    label = element.getAttribute(\"class\");
                }
                if (!label) {
                    label = element.getAttribute(\"value\");
                }
                if (!label) {
                    label = element.text;
                }
                if (label) {
                    label = label.replace(/\\s{2,}/gi, ' ').replace(/['\"]+/g, '').replace(/\\n/g, ' ');
                } 
                return label;
            }
            
            function findElementByXpath(pattern, contextNode) {
                if (contextNode === undefined) {
                  var xpathResult = document.evaluate(pattern, document, null, XPathResult.ANY_TYPE, null);
                } else {
                  var xpathResult = document.evaluate(pattern, contextNode, null, XPathResult.ANY_TYPE, null);
                }
                return xpathResult.iterateNext();
            }

            elements = collect(\"%s\");
            return createNodes(elements);
            """ % xpath_str

        collected = self.driver.execute_script(script)

        return collected

    def collect(self):
        """
        collects actionable elements

        :return: a list of actionable elements
        """
        collected = []
        for pattern in self.xpath_patterns:
            elements = self.driver.find_elements_by_xpath(pattern)
            if elements:
                collected.extend(elements)
        return collected

    def parse(self, elements):
        """
        statically analyzes the elements

        :param elements: collected elements
        :return: parsed node
        """
        node_metrics = NodeMetrics()
        node_metrics.available = len(elements)

        nodes = []
        for element in elements:
            node = Node(self.driver.current_url)
            if node.parse(element):
                nodes.append(node)

        node_metrics.visible = len(nodes)
        return nodes, node_metrics

    def analyze(self):
        # collect
        elements = self.collect_js()

        # parse
        return self.parse(elements)
