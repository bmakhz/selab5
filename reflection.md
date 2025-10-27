1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest fixes were removing eval() and replacing the bare except:.
These were single-line changes that had a high impact on security and robustness.
The hardest fix was removing the global stock_data variable.
This required refactoring the entire script into a class (InventorySystem)
to properly manage the application's state.

2. Did the static analysis tools report any false positives? If so, describe one example.

No, in this case, there were no clear false positives.
All the issues flagged by the tools were valid. The security warnings,
bug warnings, and major style warnings all pointed to real problems
that made the code less secure, robust, or maintainable.

3. How would you integrate static analysis tools into your actual software development workflow?

Local Development: Integrate tools like Flake8 directly into the code editor
for real-time feedback.
Pre-Commit Hooks: Use a pre-commit hook to automatically run fast tools
like Flake8 and Bandit to block any new code with errors.
Continuous Integration (CI): Run a full static analysis (Pylint, Bandit)
as a required step in the CI pipeline to fail the build.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Robustness: The code is significantly more robust. The eval() security hole
is gone, the logs=[] bug is fixed, and error handling is now specific
(except KeyError:) so it won't hide other bugs.
Readability: The new class structure (InventorySystem) is much cleaner and
easier to understand than loose functions relying on a global variable.
Maintainability: By removing the global state, the code is now encapsulated,
making it far easier to test, debug, and add new features.