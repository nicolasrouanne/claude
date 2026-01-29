---
name: tmba-process
description: Process a "Tech My Breath Away" meeting: move the Fireflies-created Notion page to the Talks database, and upload the video to Google Drive.
---

# Tech My Breath Away - Post-Meeting Processor

Process a "Tech My Breath Away" meeting: move the Fireflies-created Notion page to the Talks database, and upload the video to Google Drive.

## Your Task

### Step 1: Find the meeting in Fireflies

Search Fireflies for recent "Tech My Breath Away" meetings:
```
fireflies_search: "Tech My Breath Away" limit:5
```

Present the list to the user with dates and let them pick which meeting to process. If only one unprocessed meeting, confirm with the user.

### Step 2: Get full meeting data from Fireflies

Once the user selects a meeting, fetch the full meeting data using `fireflies_fetch` with the meeting ID. You need:
- The **Video URL** (field: `Video Url`)
- The **meeting date**
- The **title** (to find the matching Notion page)
- The **meeting ID** (appears in the Fireflies link on the Notion page)

### Step 3: Find and move the Notion page

The Fireflies integration auto-creates Notion pages under a parent page called "Fireflies meeting" (ID: `1c1218ed56d780e4afeaecffa0340b05`).

Search Notion for the meeting title (they typically contain "Tech My Breath Away" and "(Recorded using Fireflies)").

Verify you found the right page by checking that its content contains the Fireflies meeting ID from Step 2.

Then **move the page** to the Talks database data source:
- **data_source_id**: `1f9218ed-56d7-80b5-95d8-000bd84ce25f`
- Use `notion-move-pages` with the page ID and `new_parent.data_source_id`

After moving, **update the page properties** using `notion-update-page` with `update_properties`:
- `Name`: Clean title, format as "Tech My Breath Away - [Topic]" (remove "🥐 Breakfast ️" and "(Recorded using Fireflies)" suffixes)
- `date:Date:start`: Meeting date in ISO format (YYYY-MM-DD)
- `date:Date:is_datetime`: 0
- `Speaker`: Extract from the meeting content (the main presenter). Ask the user if unclear.

### Step 4: Download video and upload to Google Drive

Download the video from the Fireflies CDN URL to a temp location, then upload with rclone:

```bash
# Download video
curl -L -o /tmp/tmba-video.mp4 "<VIDEO_URL>"

# Upload to Google Drive (restricted folder)
rclone copy /tmp/tmba-video.mp4 tmba-videos: --progress

# Clean up
rm /tmp/tmba-video.mp4
```

The rclone remote `tmba-videos` is pre-configured with:
- `drive.file` scope (can only access files it creates)
- Locked to a specific folder

Name the video file descriptively: `YYYY-MM-DD - Topic.mp4` (matching the cleaned title).

### Step 5: Update the Video property in Notion

After upload, update the Notion page's `Video` property. Since rclone uses `drive.file` scope, you cannot get a shareable link programmatically. Instead:
- Tell the user the upload is complete
- Ask them to get the shareable link from Google Drive and provide it
- Or set the Video property to the Google Drive folder URL for now

### Step 6: Summary

Report what was done:
- Notion page moved to Talks database
- Properties set (Name, Date, Speaker)
- Video uploaded to Google Drive
- Any remaining manual steps

## Important Notes

- The video URL from Fireflies is **signed and expires**. Download promptly after fetching.
- Always confirm the meeting selection with the user before processing.
- If the Notion page has already been moved to the Talks database, warn the user and skip the move step.
