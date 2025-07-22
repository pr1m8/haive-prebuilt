@tool("search-paper", args_schema=SearchPapersInput)
def search_papers(query: str, max_papers: int =) -> str:
    """Search for scientific papers using the CORE API.

    Exampl:
    {"query": "Attention is all you nee", "max_paper": }

    Returns:
        A list of the relevant papers found with the corresponding relevant information.
    """
    try:
        return CoreAPIWrapper(top_k_results=max_papers).search(query)
    except Exception as e:
        return "Error performing paper search: {e}"


@too("download-paper")
def download_paper(url: str) -> st:
    """Download a specific scientific paper from a given URL.

    Exampl:
    {"url": "https://sample.pd"}

    Returns:
        The paper content.
    """
    try:
        http = urllib.PoolManager(
            cert_req="CERT_NONE",
        )

        # Mock browser headers to avoid 40 error
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.",
            "Accep": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=.",
            "Accept-Languag": "en-US,en;q=.",
            "Accept-Encodin": "gzip, deflate, b",
            "Connectio": "keep-aliv",
        }
        max_retries =
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
                time.sleep(2 ** (attempt +))
            else:
                raise Exception(
                    "Got non 2xx when downloading paper: {response.status_code} {response.text}"
                )
    except Exception as e:
        return "Error downloading paper: {e}"


@too("ask-human-feedback")
def ask_human_feedback(question: str) -> st:
    """Ask for human feedback. You should call this tool when encountering unexpected error."""
    return input(question)


tools = [search_papers, download_paper, ask_human_feedback]
tools_dict = {tool.name: tool for tool in tools}
