# make first part as simple sequence and own agent graph
# https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/systematic_review_of_scientific_articles.ipynb
class SystemicReviewOfScientificArticlesAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def set_workflow(self) -> None:
        self.graph.add_node("process_inpu", process_input)
        self.graph.add_node("planne", plan_node)
        self.graph.add_node("researche", research_node)
        self.graph.add_node("search_article", take_action)
        self.graph.add_node("article_decision", decision_node)
        self.graph.add_node("download_article", article_download)
        self.graph.add_node("paper_analyze", paper_analyzer)

        self.graph.add_node("write_abstrac", write_abstract)
        self.graph.add_node("write_introductio", write_introduction)
        self.graph.add_node("write_method", write_methods)
        self.graph.add_node("write_result", write_results)
        self.graph.add_node("write_conclusio", write_conclusion)
        self.graph.add_node("write_reference", write_references)

        self.graph.add_node("aggregate_pape", aggregator)
        self.graph.add_node("critique_pape", critique)
        self.graph.add_node("revise_pape", paper_reviser)
        self.graph.add_node("final_draf", final_draft)

        self.graph.add_edge("process_inpu", "planne")
        self.graph.add_edge("planne", "researche")
        self.graph.add_edge("researche", "search_article")
        self.graph.add_edge("search_article", "article_decision")
        self.graph.add_edge("article_decision", "download_article")
        self.graph.add_edge("download_article", "paper_analyze")

        self.graph.add_edge("paper_analyze", "write_abstrac")
        self.graph.add_edge("paper_analyze", "write_introductio")
        self.graph.add_edge("paper_analyze", "write_method")
        self.graph.add_edge("paper_analyze", "write_result")
        self.graph.add_edge("paper_analyze", "write_conclusio")
        self.graph.add_edge("paper_analyze", "write_reference")

        self.graph.add_edge("write_abstrac", "aggregate_pape")
        self.graph.add_edge("write_introductio", "aggregate_pape")
        self.graph.add_edge("write_method", "aggregate_pape")
        self.graph.add_edge("write_result", "aggregate_pape")
        self.graph.add_edge("write_conclusio", "aggregate_pape")
        self.graph.add_edge("write_reference", "aggregate_pape")
        self.graph.add_edge("aggregate_pape", "critique_pape")

        self.graph.add_conditional_edges(
            "critique_pape",
            exists_action,
            {
                "final_draf": "final_draf",
                "revis": "revise_pape",
                True: "search_article",
            },
        )

        self.graph.add_edge("revise_pape", "critique_pape")
        self.graph.add_edge("final_draf", END)

        self.graph.set_entry_point("process_inpu")  # "ll"
