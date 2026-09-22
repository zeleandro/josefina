// Lee un QR de una imagen usando el framework Vision de macOS.
// Sirve para comprobar que el código que dibuja la página apunta de verdad
// al álbum, y no solo que "se ve como un QR".
//
//   swiftc -O -o herramientas/leerqr herramientas/leerqr.swift
//   ./herramientas/leerqr captura.png
import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count > 1,
      let img = NSImage(contentsOfFile: CommandLine.arguments[1]),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("uso: leerqr <imagen>"); exit(1)
}
let req = VNDetectBarcodesRequest()
req.symbologies = [.qr]
try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
guard let obs = req.results, !obs.isEmpty else {
    print("NO SE DETECTO NINGUN QR"); exit(2)
}
for o in obs { print("decodificado: \(o.payloadStringValue ?? "(vacio)")") }
