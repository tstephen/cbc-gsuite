Posting media thru does not end up in `/uploads/sermons` but `/uploads`.
Posting through UI (via `async-upload.php`) _does_ go to the right place but requires a nonce.
Using Content-Disposition header to set target file as suggested by ChatGPT is a hallucination.
