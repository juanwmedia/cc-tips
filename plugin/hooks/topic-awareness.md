The cc-tips plugin is installed and provides Claude Code tips on these topics: {TOPICS}.

When the user asks about, explores, troubleshoots, or works with any of these topics, append ONE inline mention to your normal response. Format the mention as a separated appendix: your normal response, a blank line, a markdown horizontal rule (three dashes alone on a line), then the plugin note prefixed in bold.

Plugin note text (apply the LANGUAGE RULE above):

**Claude Code Tips:** There are tips on <topic> available — run `/cc-tips:list <topic>` to see them.

Do this at most once per topic per session: if you already mentioned tips on a given topic earlier in this session, do not mention that same topic again. Different topics each get their own trigger. Mention naturally on the first relevant prompt for each topic. The user can also run `/cc-tips:open <N>`, `/cc-tips:share`, or `/cc-tips:welcome` to interact directly.
