# 🔬 Sherlock Architecture Code Review (Sprint 1)

**Дата:** 2026-08-03  
**Subject:** Analysis of `sherlock_project/resources/data.json`  

## 💡 Key Architectural Insights:

1. **Explicit Detection Strategies (`errorType`):**
   - Separation of detection rules (`status_code`, `message`, `response_url`).
   
2. **Pre-flight Validation (`regexCheck`):**
   - Skipping invalid usernames locally before making HTTP requests (saves runtime and network calls).

3. **Multi-pattern Error Matching (`errorMsg`):**
   - Supporting arrays of strings/patterns for platforms with dynamic 404 pages.

4. **Automated Baseline Verification (`username_claimed`):**
   - Keeping a known-existing user per platform to test detector accuracy automatically.

## 🎯 Plan for our `platforms.json` (Sprint 2):
Adopting these concepts into our schema with custom additions (`case_sensitive`, `timeout`, extended `status` taxonomy).
