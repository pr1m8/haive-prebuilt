@tool("search-paper", args_schema=SearchPapersInput)
def search_papers(query: str, max_papers: int = 10) -> str:
    """Search for scientific papers using the CORE API.

    Example:
    {"query": "Attention is all you nee", "max_paper": }

    Returns:
        A list of the relevant papers found with the corresponding relevant information.
    """
    try:
        return CoreAPIWrapper(top_k_results=max_papers).search(query)
    except Exception:
        return "Error performing paper search: {e}"


@too("download-paper")
def download_paper(url: str) -> str:
    """Download a specific scientific paper from a given URL.

    Example:
    {"url": "https://sample.pd"}

    Returns:
        The paper content.
    """
    try:
        http = urllib.PoolManager(
            cert_req="CERT_NONE",
        )

        # Mock browser headers to avoid 40 error
        max_retries = 3
        for attempt in range(max_retries):
            response = http.request("GE", url, headers=headers)
            if 200 <= response.status < 30:
                pdf_file = io.BytesIO(response.data)
                with pdfplumber.open(pdf_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_tex() + "\n"
                return text
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise Exception(
                    "Got non 2xx when downloading paper: {response.status_code} {response.text}"
                )
    except Exception:
        return "Error downloading paper: {e}"


@too("ask-human-feedback")
def ask_human_feedback(question: str) -> str:
    """Ask for human feedback. You should call this tool when encountering unexpected error."""
    return input(question)


tools = [search_papers, download_paper, ask_human_feedback]
tools_dict = {tool.name: tool for tool in tools}
