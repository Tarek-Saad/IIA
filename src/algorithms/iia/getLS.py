from src.algorithms.iia.Pop_index_LO_match import GetLOMatching
from src.core.services.ExtractFromLOs import ExtractFromLOs
from src.core.services.GetlearnersServices import LearnerServices

class getLS:
    def __init__(self):
        pass

    def LOsLS(self ,learning_goals , knowledge_base ):
        GetLOMatchingOBJ = GetLOMatching()
        result = GetLOMatchingOBJ.getLOMatch(learning_goals, knowledge_base)

        ExtractFromLOsOBJ = ExtractFromLOs()
        all_paths_learning_styles =ExtractFromLOsOBJ.extract_learning_styles_for_paths(result['selected_los'])


        return {"LSs":all_paths_learning_styles , "LOs":result['selected_los'] , "chromosomes":result['chromosomes']}

    def LearnerLS(self , email):
        LearnerServicesOBJ = LearnerServices()
        learner_learning_styles = LearnerServicesOBJ.get_learner_learning_styles(email)
        return learner_learning_styles


if __name__ == "__main__":
    LS_service = getLS()

    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]

    print("\n" + "="*60)
    print("🚀 Starting Learning Object & Learning Style Extraction Process")
    print("="*60)

    # Fetch the learning objects, their learning styles, and chromosomes
    result = LS_service.LOsLS(learning_goals, knowledge_base)

    print("\n🎯 Learning Goals:", learning_goals)
    print("🎯 Knowledge Base:", knowledge_base)

    print("\n" + "-"*60)
    print("🔍 Extracted Learning Styles for Each Path")
    print("-"*60)

    for idx, path_ls in enumerate(result['LSs'], 1):
        print(f"\n🛣️  Path {idx}:")
        for concept_idx, ls in enumerate(path_ls, 1):
            print(f"   🔹 Concept {concept_idx} Learning Styles:")
            print(f"       ▪ LS1 (Active/Reflective): {ls['LS1']}")
            print(f"       ▪ LS2 (Visual/Verbal):    {ls['LS2']}")
            print(f"       ▪ LS3 (Sensing/Intuitive): {ls['LS3']}")
            print(f"       ▪ LS4 (Sequential/Global): {ls['LS4']}")

    print("\n" + "-"*60)
    print("📦 Selected Learning Objects (LOs) for Each Path")
    print("-"*60)

    for idx, path_los in enumerate(result['LOs'], 1):
        print(f"\n🛣️  Path {idx}:")
        for concept_idx, lo in enumerate(path_los, 1):
            print(f"   🔹 Concept {concept_idx} LO:")
            print(f"       ▪ Name:         {lo.get('name', 'Unknown')}")
            print(f"       ▪ LO ID:        {lo.get('lo_id', 'N/A')}")
            print(f"       ▪ Difficulty:   {lo.get('difficulty', 'N/A')}")
            print(f"       ▪ Format:       {lo.get('formatt', 'N/A')}")
            print(f"       ▪ Source:       {lo.get('sourcee', 'N/A')}")

    print("\n" + "-"*60)
    print("🧬 Chromosomes Representation for Each Path")
    print("-"*60)

    for idx, chromosome in enumerate(result['chromosomes'], 1):
        print(f"\n🛣️  Path {idx}: Chromosome: {chromosome}")

    print("\n" + "="*60)
    print("✅ Data Extraction Complete")
    print("="*60)

    # Retrieve learner learning styles
    email_to_search = 'kareem@example.com'
    learning_styles = LS_service.LearnerLS(email_to_search)

    print("\n" + "="*60)
    print(f"🎓 Learner Learning Styles for {email_to_search}")
    print("="*60)

    if learning_styles:
        print(f"   ▪ LS1 (Active/Reflective): {learning_styles['LS1']}")
        print(f"   ▪ LS2 (Visual/Verbal):    {learning_styles['LS2']}")
        print(f"   ▪ LS3 (Sensing/Intuitive): {learning_styles['LS3']}")
        print(f"   ▪ LS4 (Sequential/Global): {learning_styles['LS4']}")
    else:
        print("❌ No learning styles found for this email.")

    print("\n" + "="*60)
    print("🎉 Process Completed Successfully")
    print("="*60)