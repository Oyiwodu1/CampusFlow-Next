## ENGINEER B - OMALE MOSES

Problem: In reports.py I didn't know if the resolution percentage include the % sign in its return value.

Initial understanding: returning "25.0%" is convenient for printing.

What I verified: the value gets used in the CLI's f"{...}" format string, so returning a string would double the %; also tests can't compare strings to numbers.

Decision: I rejected the string return, kept float, then added a regression test.

### Final Individual Reflection — Fellow: Engineer B (Search, Reporting, and CLI Engineer)

1. **Which feature did you personally implement, and how do you know it works?**
   I personally implemented the cumulative multi-filter search engine (`search_tickets`), the enhanced category and percentage reporting dashboard (`generate_detailed_report`), and the decoupled quiz scoring logic (`score_answers`). I know they work because I wrote a rigorous automated unit test suite inside `tests/test_search.py` and `tests/test_reports.py` that asserts successful criteria isolation, tests edge-case string mutations (whitespace stripping, casefolding), protects against `ZeroDivisionError` on blank lists, and checks dictionary metadata layout integrity. All tests passed cleanly with an 'OK' status on the terminal.

2. **What did AI teach you that you did not understand at the start?**
   AI taught me how to separate data structures from display execution logic to build purely testable engines. Before the sprint, I would have put interactive `input()` or `print()` lines directly inside the quiz scoring logic. AI showed me how to pass data payloads as lists of strings (`submitted`) into a standalone mathematical function (`score_answers`). This allowed me to test data structures and calculations dynamically without forcing automated test runners to stall for human keyboard commands.

3. **Give one example where you verified, changed, or rejected an AI suggestion.**
   When building the case-insensitive title search engine, an initial concept suggested string processing via `.lower()`. After auditing this suggestion against the strict punctuation guidelines in section 1.2, I rejected a simple character match and instead implemented explicit string extraction combining `.strip().casefold()`. This ensured that queries with leading or trailing spaces are normalized while strictly preserving internal punctuation distinctions (like forcing a hyphen check for 'wi-fi'), matching the exact product specification rules.

