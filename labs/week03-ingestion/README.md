# Week 03 Lab

Build an ingestion pipeline from a public API/dataset; handle errors and retries.

Starter files for this week's lab will be added here before the lab session
(pulled into your repo via `git fetch upstream && git merge upstream/main`,
as introduced in the Week 1 lab).
## Reflection Questions

1. **Which failure type was easiest/hardest to trigger, and why?**
   - **Easiest:** The HTTP 400 Bad Request error was the easiest to trigger by passing invalid coordinates (e.g., `latitude=999`). It fails deterministically on the server side every time.
   - **Hardest:** Real connection errors and timeout failures without mock objects were the hardest to trigger, as they depend on unpredictable external network conditions and server availability[cite: 2].

2. **How did exponential backoff change the timing between retry attempts? What did you observe in the printed delays?**
   - Exponential backoff doubled the wait duration after each failed attempt using the formula `delay = BASE_DELAY * (2 ** (attempt - 1))`[cite: 2].
   - In the printed terminal output, the delays increased sequentially from 1s to 2s, then 4s, and finally 8s before the script gave up[cite: 2]. This spacing gives transient network glitches or high server loads time to recover without overloading the API endpoint[cite: 2].

3. **Why did we deliberately not retry on HTTP 400?**
   - An HTTP 400 status code represents a client-side error indicating an invalid payload, bad parameter syntax, or malformed request structure[cite: 2]. As covered in lecture, 4xx errors are deterministic failures; repeating the exact same request will always return a 400 and waste network/compute resources while risking rate limits or API blocks[cite: 2]. Conversely, timeouts and connection errors are transient server or network issues that can succeed upon retrying[cite: 2].

4. **What to specify in a data contract for downstream consumers?**
   - **Schema:** Explicit list of JSON keys, expected nesting structure, and precise data types (e.g., `latitude` as float, `temperature_2m` as float)[cite: 2].
   - **Semantics:** Clear unit descriptions for physical values (e.g., temperatures in Celsius, wind speeds in km/h)[cite: 2].
   - **SLA:** Delivery frequency, expected landing location (`data/raw/`), availability guarantees, and file naming conventions[cite: 2].
   - **Change Management:** A versioning policy and formal advance notice / deprecation protocol prior to renaming, modifying, or deleting schema fields so downstream pipelines do not break silently[cite: 2].