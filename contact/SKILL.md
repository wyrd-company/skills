---
name: contact
description: >
  Use when you need to reach a person outside the thread: an alert, a notification, or a reply you wait for. Covers `pushover` for alerts to a named person, and `ntfy` for notifications and replies. Not for messaging another agent or thread.
---

You have 2 tools at your disposal for contacting the user outside of your conversation/thread:

- `pushover`: Use this for alerts to specific users.
- `ntfy`: Use this for general notifications.

## Pushover

Use the workspace `pushover` CLI to send push notifications. Run
`pushover --help` for all options.

```bash
pushover --list-recipients
pushover --recipient boblangley --title 'Input needed' --message 'The plan is ready for your review.'

# Include a link the user can open from the notification.
pushover --recipient <operator> --title 'Review ready' --message 'Please review the proposed changes.' \
  --url 'https://github.com/owner/repo/pull/123' --url-title 'Open pull request'
```

`--recipient` and `--message` are required; `--title`, `--url`, and `--url-title`
are optional. Use `boblangley` for Bob and `iradesa` for Katelyn, provided their
secrets have been provisioned. `--list-recipients` shows the supported names;
omitting the recipient also lists them and exits with an error without sending.
Choose the recipient from the task context; ask if the intended person is
unclear. Do not infer the recipient from the current Git operator.
Quote message text to preserve spaces and shell characters. `--device` can
target named Pushover devices; by default the notification goes to all devices.
The default priority is `0` (normal). Use `--priority 1` sparingly for urgent
notifications. Priority `2` repeats emergency alerts and should only be used
when explicitly requested.

Credentials load automatically from OpenBao at
`kv/workspace/pushover/<recipient>`, fields `user_key` and `app_token`, through
the Wyrwood socket configured by `BAO_ADDR`.
No `--user`, `--token`, local credential file, or container login is needed.
If access returns `403`, report that the workspace's Wyrwood policy needs read
access to `kv/data/workspace/pushover/*` and list access to
`kv/metadata/workspace/pushover`; do not seek alternate credentials.

Exit status `0` means Pushover accepted the notification, not that the user read
it. Report failures; avoid blind retries after a timeout because the original
notification may already have been accepted. Pushover does not provide a reply
subscription through this CLI; use the ntfy flow below when waiting for a reply.

## ntfy

`ntfy --help`

### Publishing a notification

```bash
ntfy pub <topic> <message>
# OR
cat message.txt | ntfy pub <topic>
```

You can use the `--tags` to add emojis or other tags.

You can add the `--click` to add a URL that will open when the user clicks the notification. This goes well with the `postplan` skill.

`--priority` allows you to set the priority of the notification (use with caution).

### Subscribing to a topic

```bash
ntfy sub <topic> | head -n 1
# OR
timeout <n> ntfy sub <topic> | head -n 1
```

This will subcribe to the topic and stop when the first notification arrives for the topic. If you have a way to subscribe and react to multiple notifications you can forgo the `head` command.

Make sure you call this in a way that will wake you when a reply is recieved or there is a timeout.

The timeout time should take into account the current time:

- The user is likely asleep between at least 10pm PST and 6am PST. During this time set the timeout to end at 6:30am. 
- Monday through Friday the user works during the day and may be slower to respond. Set your timeout to 1 hour.
- All other times set it to 30 minutes.
