import UIKit
import WebKit

/// Oyunun tamamı uygulamanın içindeki `www` klasöründen, internete çıkmadan açılır.
/// Dosyalar `bakkal://game/...` adresinden verilir: `file://` yerine kendi adresimiz olunca
/// localStorage (oyun kaydı) kalıcı olur ve müzik dosyaları parça parça (Range) okunabilir.
final class GameViewController: UIViewController, WKNavigationDelegate {
  static let scheme = "bakkal"
  private var webView: WKWebView!

  override var prefersStatusBarHidden: Bool { true }
  override var supportedInterfaceOrientations: UIInterfaceOrientationMask { .portrait }
  override var preferredScreenEdgesDeferringSystemGestures: UIRectEdge { .bottom }

  override func loadView() {
    let config = WKWebViewConfiguration()
    config.setURLSchemeHandler(BundleSchemeHandler(), forURLScheme: Self.scheme)
    config.allowsInlineMediaPlayback = true
    config.mediaTypesRequiringUserActionForPlayback = []
    config.websiteDataStore = .default()

    let web = WKWebView(frame: .zero, configuration: config)
    let background = UIColor(red: 0x16 / 255, green: 0x36 / 255, blue: 0x2b / 255, alpha: 1)
    web.isOpaque = true
    web.backgroundColor = background
    web.scrollView.backgroundColor = background
    web.scrollView.bounces = false
    web.scrollView.contentInsetAdjustmentBehavior = .never
    web.allowsLinkPreview = false
    web.navigationDelegate = self
    webView = web
    view = web
  }

  override func viewDidLoad() {
    super.viewDidLoad()
    webView.load(URLRequest(url: URL(string: "\(Self.scheme)://game/index.html")!))
  }

  // Oyunun dışına hiçbir adrese gidilmez.
  func webView(
    _ webView: WKWebView,
    decidePolicyFor navigationAction: WKNavigationAction,
    decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
  ) {
    decisionHandler(navigationAction.request.url?.scheme == Self.scheme ? .allow : .cancel)
  }

  // Sistem web sürecini bellek için kapatırsa oyun kayıttan yeniden açılır.
  func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
    webView.reload()
  }
}

final class BundleSchemeHandler: NSObject, WKURLSchemeHandler {
  private let root = Bundle.main.resourceURL!
    .appendingPathComponent("www", isDirectory: true).standardizedFileURL

  private static let types: [String: String] = [
    "html": "text/html; charset=utf-8",
    "js": "text/javascript; charset=utf-8",
    "css": "text/css; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "png": "image/png",
    "jpg": "image/jpeg",
    "svg": "image/svg+xml",
    "mp3": "audio/mpeg",
    "woff2": "font/woff2",
  ]

  func webView(_ webView: WKWebView, start task: WKURLSchemeTask) {
    guard let url = task.request.url else { return }
    var path = url.path
    if path.isEmpty || path == "/" { path = "/index.html" }
    let file = root.appendingPathComponent(String(path.dropFirst())).standardizedFileURL
    guard file.path.hasPrefix(root.path + "/"), let data = try? Data(contentsOf: file) else {
      task.didFailWithError(URLError(.fileDoesNotExist))
      return
    }
    var headers = [
      "Content-Type": Self.types[file.pathExtension.lowercased()] ?? "application/octet-stream",
      "Accept-Ranges": "bytes",
      "Cache-Control": "no-cache",
    ]
    var status = 200
    var body = data
    if let range = Self.byteRange(task.request.value(forHTTPHeaderField: "Range"), size: data.count) {
      status = 206
      body = data.subdata(in: range)
      headers["Content-Range"] = "bytes \(range.lowerBound)-\(range.upperBound - 1)/\(data.count)"
    }
    headers["Content-Length"] = String(body.count)
    let response = HTTPURLResponse(
      url: url, statusCode: status, httpVersion: "HTTP/1.1", headerFields: headers)!
    task.didReceive(response)
    task.didReceive(body)
    task.didFinish()
  }

  func webView(_ webView: WKWebView, stop task: WKURLSchemeTask) {}

  /// "bytes=a-b", "bytes=a-" ya da "bytes=-n" biçimindeki isteği yarı açık aralığa çevirir.
  static func byteRange(_ header: String?, size: Int) -> Range<Int>? {
    guard let header, header.hasPrefix("bytes="), size > 0 else { return nil }
    let spec = header.dropFirst(6).split(separator: ",").first ?? ""
    let parts = spec.split(separator: "-", omittingEmptySubsequences: false)
    guard parts.count == 2 else { return nil }
    let start: Int
    let end: Int
    if parts[0].isEmpty {
      guard let n = Int(parts[1]), n > 0 else { return nil }
      start = max(0, size - n)
      end = size - 1
    } else {
      guard let a = Int(parts[0]) else { return nil }
      start = a
      end = parts[1].isEmpty ? size - 1 : min(Int(parts[1]) ?? size - 1, size - 1)
    }
    guard start <= end, start < size else { return nil }
    return start..<(end + 1)
  }
}
