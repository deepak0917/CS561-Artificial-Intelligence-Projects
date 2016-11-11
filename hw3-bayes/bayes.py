#------------------------Imports--------------------------------------
import sys

#------------------------Data Structures------------------------------
class Query:
    def __init__(self):
        self.m_num_query_vars = 0
        self.m_query_vars = []
        self.m_num_observed_vars = 0
        self.m_observed_vars = []


class BayesNode:
    def __init__(self):
        self.m_name = ""
        self.m_parents = []
        self.m_probability_table = []


#------------------------Read Input File------------------------------
def ReadInputFile(in_file_name, out_queries, out_bayes_net):
    input_file = open(in_file_name)
    num_queries = int(input_file.readline())
    for i in range(num_queries):
        out_queries.append(ParseQuery(input_file.readline()))
    while True:
        new_node = ParseBayesNode(input_file)
        if new_node == None:
            break
        out_bayes_net.append(new_node)
    input_file.close()


def ParseQuery(in_query_string):
    ret_query = Query()
    inside_string = in_query_string[in_query_string.find("(") + 1:in_query_string.find(")")]
    split_string = inside_string.split("|")
    query_vars_string = split_string[0].strip()
    split_query_vars = query_vars_string.split(",")
    ret_query.m_num_query_vars = len(split_query_vars)
    for q in split_query_vars:
        query_var = q.strip()
        ret_query.m_query_vars.append(GetVariableAssignment(query_var))
    if len(split_string) > 1:
        observed_vars_string = split_string[1].strip()
        split_observed_vars = observed_vars_string.split(",")
        ret_query.m_num_observed_vars = len(split_observed_vars)
        for o in split_observed_vars:
            observed_var = o.strip()
            ret_query.m_observed_vars.append(GetVariableAssignment(observed_var))
    return ret_query


def GetVariableAssignment(in_var_string):
    split_string = in_var_string.split("=")
    return {split_string[0].strip() : split_string[1].strip()}


def ParseBayesNode(in_input_file):
    top_line = in_input_file.readline()
    if not top_line:
        return None
    ret_node = BayesNode()
    split_top_line = top_line.split("|")
    ret_node.m_name = split_top_line[0].strip()
    if len(split_top_line) > 1:
        parent_line = split_top_line[1].split()
        for p in parent_line:
            ret_node.m_parents.append(p.strip())
    num_probs = pow(2, len(ret_node.m_parents))
    for i in range(num_probs):
        probability_line = in_input_file.readline()
        split_probability_line = probability_line.split()
        probability = split_probability_line[0]
        assignment = {}
        for j in range(len(ret_node.m_parents)):
            assignment[ret_node.m_parents[j]] = split_probability_line[j+1]
        ret_node.m_probability_table.append([assignment, float(probability)])
    in_input_file.readline()
    return ret_node


#------------------------Solve Queries--------------------------------
def ProcessQuery(in_query, in_bayes_net):
    vars = []
    query_results = {}
    for n in in_bayes_net:
        AddNodeToVarsList(n, in_bayes_net, vars)
    evidence = {}
    for o in in_query.m_observed_vars:
        evidence.update(o)
    for q in in_query.m_query_vars:
        vals = []
        false_assignment = evidence.copy()
        true_assignment = evidence.copy()
        var_name = ""
        for key in q:
            var_name = key
            false_assignment.update({key : "-"})
            true_assignment.update({key : "+"})
            evidence.update(q)
            vals.append(EnumerateVars(vars, false_assignment, in_bayes_net))
            vals.append(EnumerateVars(vars, true_assignment, in_bayes_net))
        total = vals[0] + vals[1]
        query_results.update({var_name : [(vals[0] / total), (vals[1] / total)]})
    ret_val = 1.0
    for q in in_query.m_query_vars:
        for key in q:
            is_truth_assignment = True
            if q[key] == "+":
                is_truth_assignment = True
            else:
                is_truth_assignment = False
            if is_truth_assignment:
                ret_val *= query_results[key][1]
            else:
                ret_val *= query_results[key][0]
    return ret_val


def EnumerateVars(in_vars, in_evidence, in_bayes_net):
    if len(in_vars) == 0:
        return 1.0
    first_var = in_vars[0]
    rest = []
    for i in range(1, len(in_vars), 1):
        rest.append(in_vars[i])
    if first_var in in_evidence:
        probability = ComputeProbability(first_var, in_evidence, in_bayes_net)
        enumerate_rest = EnumerateVars(rest, in_evidence, in_bayes_net)
        ret_val = probability * enumerate_rest
        return ret_val
    else:
        truth_evidence = in_evidence.copy()
        truth_evidence.update({first_var : "+"})
        truth_enumeration = EnumerateVars(rest, truth_evidence, in_bayes_net)
        truth_probability = ComputeProbability(first_var, truth_evidence, in_bayes_net)
        false_evidence = in_evidence.copy()
        false_evidence.update({first_var : "-"})
        false_enumeration = EnumerateVars(rest, false_evidence, in_bayes_net)
        false_probability = ComputeProbability(first_var, false_evidence, in_bayes_net)
        truth_val = truth_probability * truth_enumeration
        false_val = false_probability * false_enumeration
        ret_val = truth_val + false_val
        return ret_val


def AddNodeToVarsList(in_node, in_bayes_net, in_vars):
    if len(in_node.m_parents) == 0:
        if in_node.m_name not in in_vars:
            in_vars.append(in_node.m_name)
    else:
        for p in in_node.m_parents:
            AddNodeToVarsList(GetNodeFromName(p, in_bayes_net), in_bayes_net, in_vars)
        if in_node.m_name not in in_vars:
            in_vars.append(in_node.m_name)


def GetNodeFromName(in_name, in_bayes_net):
    for n in in_bayes_net:
        if in_name == n.m_name:
            return n


def ComputeProbability(in_var_name, in_evidence, in_bayes_net):
    is_truth_assignment = True
    if in_evidence[in_var_name] == "+":
        is_truth_assignment = True
    else:
        is_truth_assignment = False
    node = GetNodeFromName(in_var_name, in_bayes_net)
    if len(node.m_parents) == 0:
        ret_val = node.m_probability_table[0][1]
        if is_truth_assignment:
            return ret_val
        else:
            ret_val = 1.0 - ret_val
            return ret_val
    else:
        parent_assignment = {}
        for p in node.m_parents:
            parent_assignment.update({p : in_evidence[p]})
        for row in node.m_probability_table:
            row_found = True
            row_assignment = row[0]
            for p in node.m_parents:
                if row_assignment[p] != parent_assignment[p]:
                    row_found = False
                    break
            if row_found:
                ret_val = row[1]
                if is_truth_assignment:
                    return ret_val
                else:
                    ret_val = 1.0 - ret_val
                    return ret_val



#------------------------Main-----------------------------------------
def Main():
    queries = []
    bayes_net = []
    ReadInputFile(sys.argv[1], queries, bayes_net)
    output_file = open("output.txt", "w")
    for q in queries:
        val = ProcessQuery(q, bayes_net)
        output_file.write("{0:.2f}\n".format(val))
    output_file.close()

if __name__ == "__main__":
    Main()

