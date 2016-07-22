
#------------------------Imports-------------------------
import sys


#------------------------Structs-------------------------
class Predicate:
    def __init__(self):
        self.m_raw = None
        self.m_name = None
        self.m_args = []


class Implication:
    def __init__(self):
        self.m_raw = None
        self.m_antecedent = []
        self.m_consequent = None


class Goal:
    def __init__(self):
        self.m_raw = None
        self.m_goals = []


class KnowledgeBase:
    def __init__(self):
        self.m_implications = []
        self.m_groundFacts = []


#------------------------Globals-------------------------
input_file = None
output_file = None


#------------------------Helpers-------------------------
def WriteListToFile(inList):
    global output_file
    no_dupes = list(set(inList))
    print >> output_file, sorted(no_dupes)


def GetIntersection(inList):
    return_set = []
    first_set = inList[0]
    num_sets = len(inList)
    for word in first_set:
        occurrences = 0
        for set in inList:
            for w in set:
                if w == word:
                    occurrences = occurrences + 1
                    break
        if occurrences == num_sets:
            return_set.append(word)
    return return_set


def CreatePredicate(inString):
    new_predicate = Predicate()
    new_predicate.m_raw = inString
    begin_args_loc = inString.find("(")
    end_args_loc = inString.find(")")
    new_predicate.m_name = inString[0:begin_args_loc]
    args = inString[begin_args_loc+1:end_args_loc]
    new_predicate.m_args = args.split(",")
    return new_predicate


def ParseProblem(outGoal, outKB):
    raw_goal = input_file.readline().strip()
    outGoal.m_raw = raw_goal
    split_goal = raw_goal.split("&")
    for g in split_goal:
        goal_imp = Implication()
        goal_imp.m_raw = g
        goal_imp.m_antecedent = []
        goal_imp.m_consequent = CreatePredicate(g)
        outGoal.m_goals.append(goal_imp)
    kb_size = int(input_file.readline())
    for i in range(kb_size):
        new_rule = Implication()
        raw_string = input_file.readline().strip()
        new_rule.m_raw = raw_string
        split_string = raw_string.split("=>")
        if len(split_string) == 1:
            new_rule.m_antecedent = []
            new_rule.m_consequent = CreatePredicate(split_string[0])
            outKB.m_groundFacts.append(new_rule)
        else:
            new_rule.m_consequent = CreatePredicate(split_string[1])
            lhs = split_string[0].split("&")
            for a in lhs:
                new_rule.m_antecedent.append(CreatePredicate(a))
            outKB.m_implications.append(new_rule)


def ContainsVariable(inPredicate):
    for arg in inPredicate.m_args:
        if arg == "x":
            return True


def GetVariablePosition(inPredicate):
    for idx in range(len(inPredicate.m_args)):
        if inPredicate.m_args[idx] == "x":
            return idx


def GetSubstitution(inKB, inPredicate):
    predicates = []
    for i in inKB.m_implications:
        for a in i.m_antecedent:
            if a.m_name == inPredicate.m_name:
                predicates.append(a)
        if i.m_consequent.m_name == inPredicate.m_name:
            predicates.append(i.m_consequent)
    for p in predicates:
        for idx in range(len(p.m_args)):
            if p.m_args[idx] == "x":
                return inPredicate.m_args[idx]


def FetchRelatedImplications(inKB, inQuery):
    result = []
    for imp in inKB.m_implications:
        if imp.m_consequent.m_name == inQuery.m_name:
            if len(inQuery.m_args) > 1:
                #only return when at least one arg matches other than a variable
                for idx in range(len(inQuery.m_args)):
                    if inQuery.m_args[idx] == "x":
                        continue
                    if inQuery.m_args[idx] == imp.m_consequent.m_args[idx]:
                        result.append(imp)
                        break
            else:
                result.append(imp)
    return result


def FetchRelatedFacts(inKB, inQuery):
    result = []
    for fact in inKB.m_groundFacts:
        if fact.m_consequent.m_name == inQuery.m_name:
            result.append(fact.m_consequent)
    return result



#------------------------Backchaining Functions-------------------------
def EvaluateQuery(inKB, inQuery, inSubstitution):
    global output_file
    final_results = []
    output_file.write("Query: " + inQuery.m_raw + "\n")
    if len(inQuery.m_antecedent) > 0:
        if len(inQuery.m_antecedent) == 1:
            sub_implication = Implication()
            sub_implication.m_antecedent = []
            sub_implication.m_consequent = inQuery.m_antecedent[0]
            sub_implication.m_raw = inQuery.m_antecedent[0].m_raw
            final_results = EvaluateQuery(inKB, sub_implication, inSubstitution)
            return final_results
        else:
            sub_results = []
            for antecedent in inQuery.m_antecedent:
                sub_implication = Implication()
                sub_implication.m_antecedent = []
                sub_implication.m_consequent = antecedent
                sub_implication.m_raw = antecedent.m_raw
                sub_results.append(EvaluateQuery(inKB, sub_implication, inSubstitution))
            final_results = GetIntersection(sub_results)
            return final_results
    else:
        if inSubstitution != "" or not ContainsVariable(inQuery.m_consequent):
            temp_name = inQuery.m_consequent.m_name
            temp_args = []
            for i in range(len(inQuery.m_consequent.m_args)):
                if inQuery.m_consequent.m_args[i] == "x":
                    temp_args.append(inSubstitution)
                else:
                    temp_args.append(inQuery.m_consequent.m_args[i])
            for f in inKB.m_groundFacts:
                if f.m_consequent.m_name == temp_name:
                    args_match = True
                    for i in range(len(temp_args)):
                        if f.m_consequent.m_args[i] != temp_args[i]:
                            args_match = False
                            break
                    if args_match:
                        output_file.write(inQuery.m_raw + ": True\n")
                        return [inSubstitution]
        related_implications = FetchRelatedImplications(inKB, inQuery.m_consequent)
        related_facts = FetchRelatedFacts(inKB, inQuery.m_consequent)
        for ri in related_implications:
            ri_result = EvaluateQuery(inKB, ri, inSubstitution)
            if len(ri_result) > 0:
                for result in ri_result:
                    final_results.append(result)
                break
        for rf in related_facts:
            if len(rf.m_args) == 1:
                #no need to match any args
                final_results.append(rf.m_args[0])
            else:
                if ContainsVariable(inQuery.m_consequent):
                    #need to make sure one arg matches for proper substitution
                    for idx in range(len(rf.m_args)):
                        if inQuery.m_consequent.m_args[idx] == "x":
                            continue
                        if inQuery.m_consequent.m_args[idx] == rf.m_args[idx]:
                            final_results.append(rf.m_args[GetVariablePosition(inQuery.m_consequent)])
    if len(final_results) > 0:
        if inSubstitution != "":
            filtered_results = []
            for s in final_results:
                if s == inSubstitution:
                    filtered_results.append(s)
            if len(filtered_results) > 0:
                output_file.write(inQuery.m_raw + ": True\n")
            else:
                output_file.write(inQuery.m_raw + ": False\n")
            return filtered_results
        else:
            output_file.write(inQuery.m_raw + ": True: ")
            WriteListToFile(final_results)
            return final_results
    else:
        output_file.write(inQuery.m_raw + ": False\n")
        return final_results


def RunInference(inKB, inGoalQuery):
    if len(inGoalQuery.m_goals) > 1:
        global output_file
        anyVariable = False
        success = True
        sub_results = []
        output_file.write("Query: " + inGoalQuery.m_raw + "\n")
        for g in inGoalQuery.m_goals:
            if not ContainsVariable(g.m_consequent):
                substitution = GetSubstitution(inKB, g.m_consequent)
                temp_results = EvaluateQuery(inKB, g, substitution)
                if len(temp_results) == 0:
                    success = False
            else:
                anyVariable = True
                sub_results.append(EvaluateQuery(inKB, g, ""))
        if anyVariable:
            intersection = GetIntersection(sub_results)
            if len(intersection) == 0:
                success = False
        if success == True:
            if not anyVariable:
                output_file.write(inGoalQuery.m_raw + ": True\n")
            else:
                output_file.write(inGoalQuery.m_raw + ": True: ")
                WriteListToFile(intersection)
        else:
            output_file.write(inGoalQuery.m_raw + ": False\n")
    else:
        if not ContainsVariable(inGoalQuery.m_goals[0].m_consequent):
            substitution = GetSubstitution(inKB, inGoalQuery.m_goals[0].m_consequent)
            EvaluateQuery(inKB, inGoalQuery.m_goals[0], substitution)
        else:
            EvaluateQuery(inKB, inGoalQuery.m_goals[0], "")

#------------------------Main-------------------------
def Main():
    # first parse the problem
    global input_file
    input_file = open(sys.argv[1])
    goal = Goal()
    kb = KnowledgeBase()
    ParseProblem(goal, kb)
    input_file.close()
    # now open the output file and begin solver
    global output_file
    output_file = open("output.txt", "w")
    RunInference(kb, goal)
    output_file.close()


if __name__ == "__main__":
    Main()