# Payload Contract

The Python monitor sends one JSON payload per new Instagram post.

## Fields

| Field | Type | Description |
| --- | --- | --- |
| `competitor` | string | Instagram username without `@`. |
| `post_shortcode` | string | Instagram shortcode used for deduplication. |
| `post_url` | string | Public Instagram post URL. |
| `image_url` | string | Image URL returned by Instaloader. |
| `caption` | string | Caption text truncated to 500 characters. |
| `likes` | number | Like count at scrape time. |
| `comments` | number | Comment count at scrape time. |
| `followers` | number | Profile follower count at scrape time. |
| `engagement_rate` | number | `(likes + comments) / followers * 100`. |
| `is_viral` | boolean | Whether engagement meets or exceeds the configured threshold. |
| `viral_threshold_percent` | number | Threshold used for the viral decision. |
| `taken_at` | string | UTC post timestamp from Instagram. |
| `scraped_at` | string | UTC scrape timestamp. |

## Example

```json
{
  "competitor": "competitor_one",
  "post_shortcode": "ABC123xyz",
  "post_url": "https://www.instagram.com/p/ABC123xyz/",
  "image_url": "https://instagram.example/image.jpg",
  "caption": "New launch announcement",
  "likes": 1250,
  "comments": 84,
  "followers": 42000,
  "engagement_rate": 3.18,
  "is_viral": true,
  "viral_threshold_percent": 2,
  "taken_at": "2026-05-02T09:00:00+00:00",
  "scraped_at": "2026-05-02T10:00:00+00:00"
}
```

## Google Sheets Columns

The n8n workflow maps these columns:

`Timestamp`, `Competitor`, `Post Shortcode`, `Post URL`, `Image URL`, `Caption`, `Likes`, `Comments`, `Followers`, `Engagement Rate`, `Is Viral`, `Viral Threshold`, `Taken At`.
