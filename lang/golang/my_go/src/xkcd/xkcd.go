package xkcd

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
)

type Info struct {
	Num        int    `json:"num"`
	Month      string `json:"month"`
	Year       string `json:"year"`
	Day        string `json:"day"`
	Img        string `json:"img"`
	Title      string `json:"title"`
	Transcript string `json:"transcript"`
}

const home = "https://xkcd.com/"

func FetchAll() []*Info {
	maxNum := 10 // 2145
	allComic := make([]*Info, maxNum+1)

	for i := 1; i <= maxNum; i++ {

		url := home + strconv.Itoa(i) + "/info.0.json"
		resp, err := http.Get(url)
		if err != nil {
			log.Fatal(err)
		} else {
			defer resp.Body.Close()
		}

		if resp.StatusCode != http.StatusOK {
			log.Fatalf("search query: %s", resp.Status)
		}

		if err := json.NewDecoder(resp.Body).Decode(&allComic[i]); err != nil {
			log.Fatal("JSON decode error!")
		}
	}
	return allComic
}
