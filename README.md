# MTSI website

Repository: https://github.com/raymondttumiwa/Website_MTSI

Expected Pages address: https://raymondttumiwa.github.io/Website_MTSI/

Static HTML, CSS, and JavaScript. No build or dependencies required.

## Publish for free with GitHub Pages

1. Open https://github.com/raymondttumiwa/Website_MTSI. For free GitHub Pages on a free account, the repository needs to be public.
2. Upload the contents of this folder to the repository root on `main`. Upload the extracted files, not the ZIP or the enclosing folder.
3. Open **Settings → Pages**. Set Source to **Deploy from a branch**, branch to **main**, folder to **/(root)**, and save.
4. Wait for the Pages deployment to finish. GitHub shows the live URL at https://github.com/raymondttumiwa/Website_MTSI/settings/pages. The expected address is `https://raymondttumiwa.github.io/Website_MTSI/`.

The website is public. This package includes the customer portfolio and supplier PDFs displayed on the site. Excel workbooks, reference images, and internal material notes are excluded.

## Updating the website

Edit the original Website-MTSI files, then run `python3 prepare_github_pages.py` there to refresh this export and ZIP. Upload the changed public files to the same GitHub repository; Pages redeploys automatically. Keep logos and PDF filenames unchanged unless you update their links.

## Local preview

Run `python3 -m http.server 8000` from this folder and open `http://localhost:8000`.

The contact form opens the visitor's email app with a draft addressed to `mtsi@muliatsi.co.id`; it does not need a server.
