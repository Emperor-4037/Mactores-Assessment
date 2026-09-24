# Agent Runner Lite - Take-Home Assignment

Here is my submission for the Agent Systems Product Engineer Intern take-home assignment. 

I really liked solving this assignment. It was a great way to learn how an Agentic AI is actually built in the backend, and it really drove home how writing tests before the main code helps structure the logic. In total, this took me around 8 hours to complete.

### 1. What's working
All six tasks are completed and working perfectly fine. I was able to get all 25 tests passing. There are no knowingly broken parts.

### 2. Design decisions
Before writing any code, I took some time to just explore the codebase and understand what I was building. 

For the verifier (Task 2), I looked at it almost like a DSA problem. I had to diff the expected effects against the actual effects, making sure to track which actual effects had already been "spent" so that a single actual effect couldn't accidentally satisfy two identical expectations. Figuring out that matching logic was the most fun and interesting part of the assessment for me.

For the main agent loop (Task 3), I broke it down into the exact steps: decide, check if finished, find the tool, run it through the gate, execute it, and feed the observation back. I made sure that if the AI hallucinates a tool, a tool throws an error, or a human reviewer says no, those just become observations fed back into the loop rather than crashing the run. The only things that actually stop the loop are a `FatalError` from the provider, hitting the `max_steps` limit, or the AI explicitly deciding it's done.

For idempotency in the `send_message` tool, I just added a simple `_idem` dictionary to the `Workspace` to cache keys we've already seen, so we don't accidentally send duplicate emails.

### 3. Testing approach
I followed the instructions and wrote the tests for Task 1 (the gate) and Task 2 (the verifier) **first**, before I actually wrote the functions. This was super helpful for figuring out what the code needed to do. 

For the gate, I used `@pytest.mark.parametrize` to run a bunch of different combinations (like budget boundaries and different autonomy levels) through the same test cleanly. 

For the agent loop and idempotency tests, I made sure to test the actual "world state" rather than just the return values. For example, to prove shadow mode works, I didn't just check the return value, I asserted that the actual `workspace.messages` list was empty. 

### 4. What was hardest
Task 3 (the agent loop) was definitely the hardest part for me, even though the docstring had clear instructions. I had a really hard time wrapping my head around all the different objects (`Run`, `Task`, `AgentDeps`, `Store`, etc.) being passed around. I spent a long time just clicking through different files and reading how they connected before I could actually write the code for it.

Task 4 (resilience and idempotency) also took some time to figure out. Task 6 (writing the tests for the loop) took quite a lot of time to fully understand because I had to learn how the `make_run` helper and the mock scenarios in `seed.py` worked, but once it clicked I was able to finish it. Task 5 (the API endpoint) was the easiest and I wrote it entirely on my own.

*(Note on AI Usage: As permitted by the brief, I used AI during this project to help me understand concepts, fix errors, and point me in the right direction when I got stuck. It was a great learning tool to help me navigate the architecture.)*

### 5. What I'd do next
If I had another day to work on this, I would have taken my sweet time to dive even deeper into the architecture and understand everything well enough to write the whole thing strictly on my own without needing AI help. 

After that, I would have definitely looked at the optional tasks mentioned in the brief, like:
- Adding a per-tool override on the gate (so things like sending an email could always require a human, even in autonomous mode).
- Adding structured logging to the run loop so it's easier to trace what happened. 
- Trying to write a test that drives the whole process through the FastAPI endpoints using the test client, instead of just calling `run_agent` directly. 
