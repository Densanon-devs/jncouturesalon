# JN Couture — Reviews Sourcing

**Rule:** every published quote on `reviews.html` must come from a real third-party review platform, with a link the visitor can click to verify on the source. No paraphrases, no invented "Verified Client" quotes.

## Currently published (2026-04-27)

All three are from BestProsInTown — that platform displays reviews **anonymously**, so the attribution is "Verified review · BestProsInTown · {month year}" instead of a name. Each card links to https://www.bestprosintown.com/id/hayden/j-n-couture-salon-/ where the visitor can confirm.

| Card | Date | Stylist | Source |
| --- | --- | --- | --- |
| 1 — extensions / Jill | Nov 2024 | Jill | BestProsInTown |
| 2 — color + bangs / Elle | May 2024 | Elle | BestProsInTown |
| 3 — cut / Jozee | Apr 2024 | Jozee | BestProsInTown |

The 4th card is the Nextdoor "Neighborhood Favorite 2017 / 2020 / 2022" recognition (linked to the Nextdoor page).

A "Read all Google reviews →" button below the grid points at `https://www.google.com/maps?cid=12966735111123942760` (the salon's Google listing via cid; opens in Google Maps).

## What was attempted but blocked

- **Google Maps reviews** — bot-blocked. Page renders as JS-only; WebFetch returns header-only content. We have the canonical URL via `cid=12966735111123942760` but no individual review text was directly verified.
- **Yelp** — returns HTTP 403 to non-browser fetchers. Yelp's TOS also restricts automated review reuse.
- **Facebook** — login wall on the reviews tab.

Third-party scraper sites (manereviews.com, salondiscover.com) do mirror real Google reviewer names + dates, but quotes can drift over time and we can't verify them against the live source. We do **not** publish those without browser-verification.

## How to add more (manual path)

When you want to add a Google, Yelp, or Facebook review:

1. Open the listing in a normal browser (signed-in is fine).
2. Pick a review. Copy the **reviewer's display name** (e.g. "Sarah K."), **date**, **star rating**, and the **exact quote** (no paraphrasing).
3. Drop them into a card in `reviews.html` using the same structure as the BestProsInTown cards. Source label = the platform name + month/year. The "Read on …" link points to either:
   - the review's permalink (Google reviews can be linked individually if you click "Share")
   - or the listing URL if no permalink is exposed (e.g. Yelp)
4. Commit with a message like `Add Google review by Sarah K. (May 2026)`.

## Open follow-ups

- **Real Google Place ID** (ChIJ-format): not retrieved. The current writereview link uses `?ludocid=12966735111123942760`, which works. If you want the proper `?placeid=ChIJ...` form, paste the Maps URL into Google's [Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id) and swap the param.
- **Stat numbers** at the top of `reviews.html` (4.7 Google, 87+ Google, 4.9 BestPros, 90% Facebook) come from older third-party listings. Verify against the live profiles next time you're signed in and adjust if drifted.
- **Nextdoor "Neighborhood Favorite" badges** for 2017/2020/2022 are reported by Google's snippet of Nextdoor's own meta description but were not visible on the rendered Nextdoor page during scraping. Confirm in a browser if you want to keep displaying those years.


GOOGLE REVIEWS::

**Chris Gummeson**, **4/20/26**, **5 stars**, **Alicia has been cutting my wife's hair for years. My wife is very particularly and always loves how her hair looks. Fellas, send your wife to Alisha, she'll take care of her.**

**Deanna Caviezel**, **6/15/25**, **5 stars**, **Tiffany is incredible! I absolutely love my hair now! Price: $120-140**

**Tara Dorosh**, **2025**, **5 stars**, **Jozee was fantastic! She got me in last minute and did a wonderful job on my color and cut. Highly recommend!**, **Services
Hairstyling, Hair coloring**

**Tori Larsen**, **2025**, **5 stars**, **I was skeptical of trying somewhere new after having been getting my hair done in Utah all over the place but I was so wrong. This place and especially JILL is AMAZING! Jill has the best eye for hair and she takes such good care of you. I have never loved my hair and extensions more. Jill is seriously the best and I will never go anywhere else <3**, **Services
Hairstyling, Hair coloring, Haircut, Hair extensions, Hair highlighting**

**Adaire Noonan (Izzy Moone)**, **2024**, **5 stars**, **They were able to fit me in to cut my hair. I loved how she cut it. It came out perfect. Will have to make an appointment for touch ups.**

**Mary West**, **2021**, **5 stars**, **Jill is the BEST. SHE'S determined to meet her customers needs.**

YELP REVIEWS::

**Denise S.**, **5/20/2024**, **5 stars**, **I am an older lady who has red hair. I needed not only to have my hair color refreshed, changed, I also am going from a long hair and wanted bangs. Elle was wonderful. She walked me through everything, chose that perfect color for me. And made sure that I was happy with my bangs before I left. Not only the bangs, but she helped feather in the face frame. This is one of the only cuts that I've ever really been happy with when I walked out of the salon, but even more happy when I took a shower and had to do it myself and it looked great. She's fabulous! This is a beautiful salon. Very friendly people. I would recommend anyone except mean people. I came across this survey while I am trying to book an appointment with L. So have a wonderful night and I look forward to my appointment.**

**Stella Ann M.**, **2/6/2025**, **5 stars**, **Alysha by far the best in understanding what you are requesting and delivers!!! She never suggests to you what she thinks you need, but listens to you... She delivers! Also her blow outs are beautifully crafted. I'm a curly haired woman with frizz and have never had anyone make my hair look so smooth and bouncy. If you're looking for a perfect salon experience with nothing but pride with the outcome, Alisha is your perfect stylist.**

**Robin E.**, **12/10/2023**, **5 stars**, **Jill has been taking care of my hair for years! I have never been disappointed. She's the best.**

**Sarah D.**, **8/17/2018**, **5 stars**, **Jill is amazing and everyone at the salon is totally in sync. The best customer service tops off great products and the most incredible hair you've ever had. Don't think twice about coming here. Your hair will thank you!**