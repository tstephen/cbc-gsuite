package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"context"
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
	spreadsheetId := os.Args[1]
	col := os.Args[2]

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

	readRange := "Sheet1!A2:" + col + "26"
	resp, err := srv.Spreadsheets.Values.Get(spreadsheetId, readRange).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve data from sheet: %v", err)
	}

	if len(resp.Values) == 0 {
		fmt.Println("No data found.")
	} else {
		fmt.Println("<html><body><strong>LEADERS COPY, PLEASE EDIT AS NEEDED AND BCC TO CONGREGATION</strong><p>Hi everyone,</p><p>Here's the plan for this Sunday. If you have any issues please try to arrange a swap.")
		fmt.Println("<ul>")
		for _, row := range resp.Values {
			if len(row) > 0 && row[len(row)-1] != "-" {
				fmt.Printf("<li><b>%s:</b> %s\n", row[0], row[len(row)-1])
			}
		}
		fmt.Println("</ul>")
	}

	// Calculate next column
	alpha := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	col2a := ""
	if len(col) > 1 {
		col2a = string(alpha[strings.Index(alpha, col)/26])
		col = string(col[1])
	}
	colIdx := strings.Index(alpha, col)
	//log.Printf("  col idx is %d", colIdx);
	colIdx2 := (colIdx + 1) % 26
	//log.Printf("  next col idx is %d", colIdx2);
	if colIdx2 == 0 {
		col2a = "A"
	}
	col2b := string(alpha[colIdx2])
	//log.Printf("  next col is %s", col2b);
	col2 := col2a + col2b
	//log.Printf("  next col is %s", col2);
	//log.Printf("  next col is %s", col2);
	readRange2 := "Sheet1!A2:" + col2 + "26"
	resp2, err2 := srv.Spreadsheets.Values.Get(spreadsheetId, readRange2).Do()

	if err2 != nil || len(resp2.Values) == 0 {
		fmt.Println("<p>No data found about next week at this stage.</p>")
	} else {
		fmt.Printf("<p><em>Looking ahead to next week, ")
		for i, row := range resp2.Values {
			if i == 1 {
				//log.Printf("  rows found: %d", len(row));
				fmt.Printf("%s will be leading worship ", row[len(row)-1])
			}
			if i == 14 {
				fmt.Printf("and %s preaching.</em></p>\n", row[len(row)-1])
			}
		}
	}

	fmt.Println("<p>Thanks as always for your service to our congregation.</p>")
	fmt.Printf("<p>The master list is: <a href='https://docs.google.com/spreadsheets/d/%s/'>here.</a></p>\n", spreadsheetId)
	fmt.Println("<p>All the best,</body></html>")
}