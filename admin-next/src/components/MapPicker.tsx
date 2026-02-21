"use client";

import { useCallback, useEffect } from "react";
import { MapContainer, TileLayer, useMapEvents, Marker, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const DEFAULT_CENTER: [number, number] = [41.2995, 69.2401]; // Ташкент

// Фикс иконки маркера в Next.js (избегаем 404 по marker-icon.png)
const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

function MapClickHandler({
  onLatLngChange,
}: {
  onLatLngChange: (lat: number, lng: number) => void;
}) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      onLatLngChange(lat, lng);
    },
  });
  return null;
}

function CenterUpdater({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  useEffect(() => {
    if (!Number.isNaN(lat) && !Number.isNaN(lng)) {
      map.setView([lat, lng], map.getZoom());
    }
  }, [lat, lng, map]);
  return null;
}

type MapPickerProps = {
  latitude: string;
  longitude: string;
  onLatitudeChange: (v: string) => void;
  onLongitudeChange: (v: string) => void;
};

export default function MapPicker({
  latitude,
  longitude,
  onLatitudeChange,
  onLongitudeChange,
}: MapPickerProps) {
  const lat = parseFloat(latitude);
  const lng = parseFloat(longitude);
  const hasValidCoords = !Number.isNaN(lat) && !Number.isNaN(lng);
  const center: [number, number] = hasValidCoords ? [lat, lng] : DEFAULT_CENTER;

  const handleLatLngChange = useCallback(
    (newLat: number, newLng: number) => {
      onLatitudeChange(String(newLat));
      onLongitudeChange(String(newLng));
    },
    [onLatitudeChange, onLongitudeChange]
  );

  return (
    <div className="space-y-2">
      <p className="text-sm font-medium text-slate-700">
        Кликните на карте, чтобы подставить широту и долготу
      </p>
      <div className="h-[240px] overflow-hidden rounded-lg border border-slate-200 sm:h-[320px]">
        <MapContainer
          center={center}
          zoom={hasValidCoords ? 16 : 12}
          style={{ height: "100%", width: "100%" }}
          scrollWheelZoom
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapClickHandler onLatLngChange={handleLatLngChange} />
          <CenterUpdater lat={hasValidCoords ? lat : DEFAULT_CENTER[0]} lng={hasValidCoords ? lng : DEFAULT_CENTER[1]} />
          {hasValidCoords && <Marker position={[lat, lng]} />}
        </MapContainer>
      </div>
    </div>
  );
}
