package main

import (
        "encoding/json"
        "fmt"
        "io/ioutil"
        "log"
        "net/http"
        "os"

        "golang.org/x/net/context"
        "golang.org/x/oauth2"
        "golang.org/x/oauth2/google"
        "google.golang.org/api/sheets/v4"
)

// Retrieve a token, saves the token, then returns the generated client.
func getClient(config *oauth2.Config) *http.Client {
        tokFile := "token.json"
        tok, err := tokenFromFile(tokFile)
        if err != nil {
                tok = getTokenFromWeb(config)
                saveToken(tokFile, tok)
        }
        return config.Client(context.Background(), tok)
}

// Request a token from the web, then returns the retrieved token.
func getTokenFromWeb(config *oauth2.Config) *oauth2.Token {
        authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
        fmt.Printf("Go to the following link in your browser then type the "+
                "authorization code: \n%v\n", authURL)

        var authCode string
        if _, err := fmt.Scan(&authCode); err != nil {
                log.Fatalf("Unable to read authorization code: %v", err)
        }

        tok, err := config.Exchange(oauth2.NoContext, authCode)
        if err != nil {
                log.Fatalf("Unable to retrieve token from web: %v", err)
        }
        return tok
}

// Retrieves a token from a local file.
func tokenFromFile(file string) (*oauth2.Token, error) {
        f, err := os.Open(file)
        defer f.Close()
        if err != nil {
                return nil, err
        }
        tok := &oauth2.Token{}
        err = json.NewDecoder(f).Decode(tok)
        return tok, err
}

// Saves a token to a file path.
func saveToken(path string, token *oauth2.Token) {
        fmt.Printf("Saving credential file to: %s\n", path)
        f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0600)
        defer f.Close()
        if err != nil {
                log.Fatalf("Unable to cache oauth token: %v", err)
        }
        json.NewEncoder(f).Encode(token)
}

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("Expected column argument")
	}
	//prog := os.Args[0]
	col := os.Args[1]

        b, err := ioutil.ReadFile("client_secret.json")
        if err != nil {
                log.Fatalf("Unable to read client secret file: %v", err)
        }

        // If modifying these scopes, delete your previously saved client_secret.json.
        config, err := google.ConfigFromJSON(b, "https://www.googleapis.com/auth/spreadsheets.readonly")
        if err != nil {
                log.Fatalf("Unable to parse client secret file to config: %v", err)
        }
        client := getClient(config)

        srv, err := sheets.New(client)
        if err != nil {
                log.Fatalf("Unable to retrieve Sheets client: %v", err)
        }

        // https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        spreadsheetId := "1vR6LybFPvSip663GMKe1Get68Fcg6oT5pGpVrOC9JQw";
        readRange := "Sheet1!A2:" + col + "23";
        resp, err := srv.Spreadsheets.Values.Get(spreadsheetId, readRange).Do()
        if err != nil {
                log.Fatalf("Unable to retrieve data from sheet: %v", err)
        }

        if len(resp.Values) == 0 {
                fmt.Println("No data found.")
        } else {
                fmt.Println("<html><body><p>Hi everyone,</p><p>Here's the plan for this Sunday. If you have any issues please try to arrange a swap.")
                fmt.Println("<ul>")
                for i, row := range resp.Values {
			if i != 11 && i != 17 && i != 18 && i != 19 {
                        // Print columns A and E, which correspond to indices 0 and 4.
                        fmt.Printf("<li><b>%s:</b> %s\n", row[0], row[len(row)-1])
			}
                }
                fmt.Println("</ul>")
                fmt.Println("<p>Thanks as always for your service to our congregation.<p>The master list is: <a href='https://docs.google.com/spreadsheets/d/1vR6LybFPvSip663GMKe1Get68Fcg6oT5pGpVrOC9JQw/edit#gid=0'>here.</a><p>All the best, Tim</body></html>")
        }
}
