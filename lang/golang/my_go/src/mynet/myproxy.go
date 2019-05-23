package myproxy

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"time"

	"golang.org/x/net/proxy"
)

const (
// proxyURL           = "localhost:1081"
// underlyingPorxyURL = "http://localhost:8001/"
// underlyingPorxyURL = "socks5://localhost:1081/"
)

// MyproxyMain ..
func MyproxyMain() {
	// dialer, err := proxy.SOCKS5("tcp", proxyURL, nil, proxy.Direct) // 拨号器
	fmt.Fprintf(os.Stdout, "input your proxy url: [default: None]")
	input := bufio.NewScanner(os.Stdin)
	input.Scan()
	underlyingPorxyURL := input.Text()

	isProxy := false
	if len(underlyingPorxyURL) != 0 { // 检测代理
		isProxy = true
	}

	client := &http.Client{}
	client.Timeout = time.Duration(5 * time.Second)

	if isProxy {
		underlyingProxy, err := url.Parse(underlyingPorxyURL)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Parse proxy url error: %s\n", err)
			os.Exit(1)
		}
		httpTransport := &http.Transport{}
		var underlyingDialer proxy.Dialer

		if underlyingProxy.Scheme != "http" && underlyingProxy.Scheme != "https" { // 处理 非HTTP 代理
			underlyingDialer, err = proxy.FromURL(underlyingProxy, proxy.Direct)
			fmt.Println("proxy: ", underlyingDialer)
			if err != nil {
				fmt.Fprintf(os.Stderr, "cannot access proxy: %s\n", err)
				os.Exit(1)
			}
			httpTransport.Dial = underlyingDialer.Dial
		} else {
			httpTransport.Proxy = http.ProxyURL(underlyingProxy)
		}
		client.Transport = httpTransport
	}

	ch := make(chan string)
	var urls = []string{
		"baidu.com", "github.com", "google.com",
		"luoyayu.cn", "apple.com", "bitbucket.org",
	}
	start := time.Now()
	for _, url := range urls {
		go fetch("https://"+url, ch, client)
	}
	for range urls {
		fmt.Println(<-ch)
	}
	fmt.Printf("%.2fs elpased\n", time.Since(start).Seconds())
}

func fetch(url string, ch chan<- string, client *http.Client) {
	start := time.Now()
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		ch <- fmt.Sprintf("cannot create request: %s\n", err)
		return
	}

	resp, err := client.Do(req) // http client do request => response
	if err != nil {
		ch <- fmt.Sprint(err)
		return
	}

	nbytes, err := io.Copy(ioutil.Discard, resp.Body) // discard body
	defer resp.Body.Close()
	if err != nil {
		ch <- fmt.Sprintf("while reading %s: %v", url, err)
		return
	}
	secs := time.Since(start).Seconds()
	ch <- fmt.Sprintf("%.2fs %7d %s", secs, nbytes, url)
}
