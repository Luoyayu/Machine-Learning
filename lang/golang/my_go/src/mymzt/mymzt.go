package mymzt

import (
	"bytes"
	"flag"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

// Main ...
func Main() {
	var year = flag.Int("y", time.Now().Year(), "year")
	var id = flag.Int("i", 0, "id")
	var host = flag.String("host", _host, "host to connect")
	var agent = flag.String("a", _userAgent, "user agent")
	var begin = flag.Int("b", 0, "id begin")
	var end = flag.Int("e", 0, "id end")
	var path = flag.String("path", "", "path to download")
	flag.Parse()
	if !(*begin <= *end && *begin != 0) {
		*begin = *id
		*end = *id
	}
	if *path != "" {
		_root = *path
	}
	for j := *begin; j <= *end; j++ {
		dlRoot := strings.Join([]string{_root, strconv.Itoa(j)}, "/")
		if _, err := os.Stat(dlRoot); !os.IsNotExist(err) {
			log.Printf("task [%4d], the dir %s is already exists, remove it.....\n", j, dlRoot)
			if err := os.RemoveAll(dlRoot); err != nil {
				log.Fatal(err)
			}
		}
		if err := os.MkdirAll(dlRoot, 0770); err != nil {
			log.Fatal(err)
		}

		url := strings.Join([]string{"http:/", *host, strconv.Itoa(*year), strconv.Itoa(j)}, "/")

		headers := map[string]string{
			"User-Agent":      *agent,
			"Host":            *host,
			"Cache-Control":   "no-store",
			"Connection":      "Keep-Alive",
			"Accept-Encoding": "gzip",
			"Content-Type":    "image/jpeg",
		}
		tot := 0
		start := time.Now()

		client := &http.Client{
			Timeout: time.Second * _maxTimeout,
		}
		var brokenImg = make([]int, 0, 10)

		tmp := bytes.Buffer{}
		for idx := 1; idx <= _max404try; idx++ {
			dlURL := strings.Join([]string{url, strconv.Itoa(idx) + ".jpg"}, "/")
			dlPath := dlRoot + "/" + strconv.Itoa(idx) + ".jpg"

			req, _ := http.NewRequest("GET", dlURL, nil)

			for key, value := range headers {
				req.Header.Set(key, value)
			}
			resp := &http.Response{}
			var err error

			broken := false
			i := 1
			for ; i <= _max54try; i++ {
				tmp.Reset()
				resp, err = client.Do(req)
				if err != nil {
					log.Printf("task [%4d], %v\n", j, err)
				} else {
					if resp.StatusCode == 404 {
						resp.Body.Close()
						if len(brokenImg) != 0 {
							log.Printf("task [%4d], when GET broken img list: %v\n", j, brokenImg)
						}
						log.Printf("task [%4d], cost %.0fs, finish download %d in %s\n",
							j, time.Since(start).Seconds(), tot, dlRoot)
						goto LoopEnd
					}

					n, _ := tmp.ReadFrom(resp.Body)
					if n < 70*1024 {
						log.Printf("task [%4d][%2d], fetching img is less than 70KB! retry......\n", j, idx)
						continue
					} else {
						break
					}
				}
			}

			if i == _max54try+1 {
				broken = true
			}

			if broken {
				log.Printf("GET broken at %s! try to use curl\n", dlURL)
				brokenImg = append(brokenImg, idx)
				cmd := exec.Command("curl", "-A", *agent, "-o", dlPath, dlURL)
				err := cmd.Start()
				if err != nil {
					log.Printf("task [%4d][%2d]%v\n", j, idx, err)
				}

			} else if resp == nil {
				log.Printf("GET error at %s!\n", dlURL)
			} else {
				jpgFile, err := os.Create(dlPath)
				if err != nil {
					log.Printf("task [%4d], %v\n", j, err)
				} else {
					n, _ := jpgFile.Write(tmp.Bytes())
					log.Printf("fetch %.0fKB %d\n", float64(n)/1024, n)
				}

				resp.Body.Close()
				jpgFile.Close()
				if err != nil {
					log.Printf("task [%4d], %v\n", j, err)
				}
				tot++
				log.Printf("finish write content to file %s\n", dlPath)
			}

		}
	LoopEnd:
		if tot == 0 {
			if err := os.RemoveAll(dlRoot); err != nil {
				log.Fatal(err)
			}
		}
	}

	//cmd := exec.Command("chown", "-R", "1000:1000", _root)
	//err := cmd.Start()
	//if err != nil {
	//	log.Fatal(err)
	//}
}
