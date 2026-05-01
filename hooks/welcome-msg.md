FIRST_RESPONSE_REQUIRED: This is the user's first session with the cc-tips plugin. Before answering the user's first prompt, render a welcome block.

English source of the welcome message (apply the LANGUAGE RULE above):

**Claude Code Tips is active.** I'll mention relevant tips contextually as you work.

Run `/cc-tips:welcome` to see all commands. _(You won't see this auto-message again.)_

Render output in this exact order:
1. The welcome message.
2. A markdown horizontal rule (three dashes alone on a line).
3. A blank line.
4. The actual response to the user's prompt.
