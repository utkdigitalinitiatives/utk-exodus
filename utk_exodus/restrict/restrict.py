import xml.etree.ElementTree as ET


class Restrictions:
    def __init__(self, policy):
        self.policy = policy
        self.ns = {"xacml": "urn:oasis:names:tc:xacml:1.0:policy"}
        self.root = self.__parse(policy)

    @staticmethod
    def __parse(policy):
        tree = ET.parse(policy)
        return tree.getroot()

    def find_rules(self):
        rules = []
        for rule in self.root.findall(".//xacml:Rule", self.ns):
            rule_id = rule.get("RuleId")
            effect = rule.get("Effect")
            rules.append((rule_id, effect))
        return rules

    def find_restricted_datastreams(self):
        restricted_datastreams = []
        for rule in self.root.findall(
            './/xacml:Rule[@RuleId="deny-dsid-mime"]', self.ns
        ):
            for resource in rule.findall(".//xacml:Resource", self.ns):
                dsid = resource.find(".//xacml:AttributeValue", self.ns).text
                restricted_datastreams.append(dsid)
        return restricted_datastreams

    def find_objects_only_accessible_by_certain_users(self):
        users_with_access = []
        for rule in self.root.findall(
            './/xacml:Rule[@RuleId="deny-access-functions"]', self.ns
        ):
            for condition in rule.findall(
                './/xacml:Condition[@FunctionId="urn:oasis:names:tc:xacml:1.0:function:not"]',
                self.ns,
            ):
                for apply in condition.findall(
                    './/xacml:Apply[@FunctionId="urn:oasis:names:tc:xacml:1.0:function:string-at-least-one-member-of"]',
                    self.ns,
                ):
                    users_with_access.append(
                        apply.find(".//xacml:AttributeValue", self.ns).text
                    )
        return users_with_access

    def determine_if_work_restricted(self):
        if len(self.find_objects_only_accessible_by_certain_users()) > 0:
            return True
        return False

    def get(self):
        return {
            "work_restricted": self.determine_if_work_restricted(),
            "restricted_datastreams": self.find_restricted_datastreams(),
        }
