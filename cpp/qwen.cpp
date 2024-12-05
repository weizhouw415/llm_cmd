#include <windows.h>
#include <winhttp.h>
#include <iostream>
#include <string>

#pragma comment(lib, "winhttp.lib")

std::string qwen_vllm_invoke(const std::wstring& server, const std::wstring& endpoint, const std::string& postData) {
    std::string response;

    // Initialize WinHTTP
    HINTERNET hSession = WinHttpOpen(L"A WinHTTP Example Program/1.0", 
                                     WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                                     WINHTTP_NO_PROXY_NAME, 
                                     WINHTTP_NO_PROXY_BYPASS, 0);

    if (hSession) {
        // Specify an HTTP server
        HINTERNET hConnect = WinHttpConnect(hSession, server.c_str(),
                                            INTERNET_DEFAULT_HTTPS_PORT, 0);

        if (hConnect) {
            // Create an HTTP request handle
            HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"POST", endpoint.c_str(),
                                                    NULL, WINHTTP_NO_REFERER, 
                                                    WINHTTP_DEFAULT_ACCEPT_TYPES, 
                                                    WINHTTP_FLAG_SECURE);

            if (hRequest) {
                // Specify the request headers
                const wchar_t* headers = L"Content-Type: application/x-www-form-urlencoded";

                // Send a request
                BOOL bResults = WinHttpSendRequest(hRequest,
                                                   headers, -1L,
                                                   (LPVOID)postData.c_str(), postData.length(),
                                                   postData.length(), 0);

                // End the request
                if (bResults) {
                    bResults = WinHttpReceiveResponse(hRequest, NULL);
                }

                // Keep checking for data until there is nothing left
                if (bResults) {
                    DWORD dwSize = 0;
                    DWORD dwDownloaded = 0;
                    LPSTR pszOutBuffer;
                    BOOL  bResults = FALSE;

                    do {
                        // Check for available data
                        dwSize = 0;
                        if (!WinHttpQueryDataAvailable(hRequest, &dwSize)) {
                            printf("Error %u in WinHttpQueryDataAvailable.\n", GetLastError());
                        }

                        // Allocate space for the buffer
                        pszOutBuffer = new char[dwSize + 1];
                        if (!pszOutBuffer) {
                            printf("Out of memory\n");
                            dwSize = 0;
                        } else {
                            // Read the data
                            ZeroMemory(pszOutBuffer, dwSize + 1);

                            if (!WinHttpReadData(hRequest, (LPVOID)pszOutBuffer, dwSize, &dwDownloaded)) {
                                printf("Error %u in WinHttpReadData.\n", GetLastError());
                            } else {
                                response.append(pszOutBuffer, dwDownloaded);
                            }

                            // Free the memory allocated to the buffer
                            delete[] pszOutBuffer;
                        }
                    } while (dwSize > 0);
                }

                // Close the request handle
                WinHttpCloseHandle(hRequest);
            }

            // Close the connect handle
            WinHttpCloseHandle(hConnect);
        }

        // Close the session handle
        WinHttpCloseHandle(hSession);
    }

    return response;
}