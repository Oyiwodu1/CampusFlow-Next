## Engineer A — Learning Entry 1: Unit Testing

Problem:  Before working on CampusFlow, I did not know what unit testing was or how to use tests to check whether my Python functions behaved correctly.

My initial understanding:  Before working on CampusFlow, I had no knowledge of unit testing. I did not know how to write tests to check whether my Python functions were working correctly. I learned about unit testing while working on this project.

Prompt to AI: I asked AI to check my understanding and guide me through adding an invalid-category test one step at a time instead of giving me the complete code.

Useful AI guidance: I learned that `self.assertIsNone()` checks whether a function returns Python's `None` value. I used it to test whether my `create_ticket()` function correctly rejects invalid inputs, such as an invalid category, invalid urgency, and a blank title.

My independent experiment/test: I wrote tests for my `create_ticket()` function with guidance from AI. I tested valid ticket creation and invalid inputs, including an invalid category, invalid urgency, and a blank title. I ran the tests myself and observed the results to check whether my function behaved as expected.

Verification source or result:I ran `python -m unittest tests.test_tickets -v`. The terminal showed that all 9 tests passed and ended with `OK`. This helped me verify that the tested ticket-creation and validation behaviours matched the expectations in my tests.

Decision:I accepted the guidance after writing and running the tests myself. Seeing all 9 tests pass helped me understand how unit tests verify specific behaviours in my ticket-creation function.

Related file/commit: tests/test_tickets.py — commit 0ccfeef (Complete ticket CLI and validation tests).

What I can now explain without AI:I learned that when a test passes, it means the particular behaviour checked by that test worked as expected. It does not mean the entire program is perfect. Different tests are needed to check different behaviours and catch possible errors.


##  EGINEER A -LEARNING ENTRY: GIT INTEGRATION

Problem: I needed to understand how to bring my teammate's merged changes into my feature branch, resolve merge conflicts, and check that the integrated project still worked.

My initial understanding: Before working on CampusFlow, I did not fully understand Git branches, pull requests, or how to bring changes from another branch into my own. I learned how to use these Git commands during the project as I worked with my teammate.

Prompt to AI: I asked AI to guide me through bringing my teammate's merged workflow changes into my feature branch safely, one step at a time.

My independent experiment/test:I ran `git fetch origin` to get the latest information from GitHub, then ran `git merge origin/main` to bring the latest changes from the main branch into my feature branch. After the merge, I ran the workflow tests to check whether Engineer B's functions worked in my local project.

Verification source or result:After merging Engineer B's changes, I ran `python3 -m unittest discover -s tests -v`. All 29 tests passed, and the terminal ended with `OK`. The tests covered ticket creation and validation, workflow, reports, and JSON storage and persistence. This helped me verify that the tested parts of the integrated project were working correctly. I still need to verify that the complete CLI works together with JSON persistence.


Useful AI guidance:I learned that `git fetch origin` retrieves the latest information about remote branches from GitHub, while `git merge origin/main` brings the changes from the remote `main` branch into my current branch. I also learned that when merge conflicts have been resolved but Git says a merge is still in progress, I need to complete the merge with a commit. After integrating my teammate's work, I learned to run the full test suite to check for problems.

Decision:I followed the Git guidance, resolved the merge conflicts, completed the merge commit, and ran the full test suite. I verified the result by checking the terminal output, which showed 29 tests passing. This helped me understand why I should test the project after integrating changes from another branch.

What I can now explain without AI: I learned that `git fetch` retrieves information about remote changes, while `git merge` brings changes from another branch into my current branch. I also learned that resolving conflicts is not always the end of a merge; Git may still require a commit to complete it. After integrating changes, I should run the tests to check that the combined code still behaves as expected.

## Engineer A — Learning Entry 3: Critically Evaluating AI Advice

Problem: While integrating Engineer B's workflow, I was about to add more menu options to `main.py`. I questioned whether I was responsible for all the integration work because we were working as a team and had separate assigned roles.