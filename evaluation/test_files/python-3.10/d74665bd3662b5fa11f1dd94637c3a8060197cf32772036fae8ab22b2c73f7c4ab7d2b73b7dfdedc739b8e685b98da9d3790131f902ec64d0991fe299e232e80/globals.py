from enum import Enum
APPLICATION_NAME = 'Boat Buddy'
APPLICATION_VERSION = '0.5.12'
LOG_FILENAME = 'BoatBuddy.log'
LOG_FILE_SIZE = 1024 * 1024
LOGGER_NAME = 'BoatBuddy'
INITIAL_SNAPSHOT_INTERVAL = 1
BUFFER_SIZE = 4096
SOCKET_TIMEOUT = 60
NMEA_TIMER_INTERVAL = 1
VICTRON_TIMER_INTERVAL = 1
GPS_TIMER_INTERVAL = 5

class SessionRunMode(Enum):
    AUTO_NMEA = 'auto-nmea'
    AUTO_VICTRON = 'auto-victron'
    AUTO_GPS = 'auto-gps'
    CONTINUOUS = 'continuous'
    INTERVAL = 'interval'
    MANUAL = 'manual'
SESSION_PAGING_INTERVAL = 60 * 60 * 24
CLOCK_PLUGIN_METADATA_HEADERS = ['UTC Time', 'Local Time']
CLOCK_PLUGIN_SUMMARY_HEADERS = ['Start Time (UTC)', 'Start Time (Local)', 'End Time (UTC)', 'End Time (Local)', 'Duration']
GPS_PLUGIN_METADATA_HEADERS = ['[SS] GPS Lat (d°m\'S" H)', '[SS] GPS Lon (d°m\'S" H)', '[SS] Location (City, Country)', '[SS] SOG (kts)', '[SS] COG (°T)', '[SS] Dst. from last entry (miles)', '[SS] Cumulative Dst. (miles)']
GPS_PLUGIN_SUMMARY_HEADERS = ['[SS] Start Location (City, Country)', '[SS] End Location (City, Country)', '[SS] Start GPS Lat (d°m\'S" H)', '[SS] Start GPS Lon (d°m\'S" H)', '[SS] End GPS Lat (d°m\'S" H)', '[SS] End GPS Lon (d°m\'S" H)', '[SS] Dst. (miles)', '[SS] Hdg. (°)', '[SS] Avg. SOG (kts)']
NMEA_PLUGIN_METADATA_HEADERS = ['[NM] True Hdg. (°)', '[NM] TWS (kts)', '[NM] TWD (°)', '[NM] AWS (kts)', '[NM] AWA (Relative °)', '[NM] GPS Lat (d°m\'S" H)', '[NM] GPS Lon (d°m\'S" H)', '[NM] Water Temp. (°C)', '[NM] Depth (m)', '[NM] SOG (kts)', '[NM] SOW (kts)', '[NM] Dst. from last entry (miles)', '[NM] Cumulative Dst. (miles)']
NMEA_PLUGIN_SUMMARY_HEADERS = ['[NM] Start Location (City, Country)', '[NM] End Location (City, Country)', '[NM] Start GPS Lat (d°m\'S" H)', '[NM] Start GPS Lon (d°m\'S" H)', '[NM] End GPS Lat (d°m\'S" H)', '[NM] End GPS Lon (d°m\'S" H)', '[NM] Dst. (miles)', '[NM] Hdg. (°)', '[NM] Avg. Wind Speed (kts)', '[NM] Avg. Wind Direction (°)', '[NM] Avg. Water Temp. (°C)', '[NM] Avg. Depth (m)', '[NM] Avg. SOG (kts)', '[NM] Avg. SOW (kts)']
VICTRON_PLUGIN_METADATA_HEADERS = ['[GX] Active Input source', '[GX] Grid 1 power (W)', '[GX] Generator 1 power (W)', '[GX] AC Input 1 Voltage (V)', '[GX] AC Input 1 Current (A)', '[GX] AC Input 1 Frequency (Hz)', '[GX] VE.Bus State', '[GX] AC Consumption (W)', '[GX] Batt. Voltage (V)', '[GX] Batt. Current (A)', '[GX] Batt. Power (W)', '[GX] Batt. SOC', '[GX] Batt. state', '[GX] PV Power (W)', '[GX] PV Current (A)', '[GX] Strt. Batt. Voltage (V)', '[GX] Tank 1 lvl (%)', '[GX] Tank 1 Type', '[GX] Tank 2 lvl (%)', '[GX] Tank 2 Type']
VICTRON_PLUGINS_SUMMARY_HEADERS = ['[GX] Batt. max voltage (V)', '[GX] Batt. min voltage (V)', '[GX] Batt. avg. voltage (V)', '[GX] Batt. max current (A)', '[GX] Batt. avg. current (A)', '[GX] Batt. max power (W)', '[GX] Batt. avg. power (W)', '[GX] PV max power (W)', '[GX] PV avg. power', '[GX] PV max current (A)', '[GX] PV avg. current (A)', '[GX] Strt. batt. max voltage (V)', '[GX] Strt. batt. min voltage (V)', '[GX] Strt. batt. avg. voltage', '[GX] AC Consumption max (W)', '[GX] AC Consumption avg. (W)', '[GX] Tank 1 max lvl', '[GX] Tank 1 min lvl', '[GX] Tank 1 avg. lvl', '[GX] Tank 2 max lvl', '[GX] Tank 2 min lvl', '[GX] Tank 2 avg. lvl']
DB_CLOCK_PLUGIN_METADATA_HEADERS = ['time_utc', 'time_local']
DB_CLOCK_PLUGIN_SUMMARY_HEADERS = ['start_time_utc', 'start_time_local', 'end_time_utc', 'end_time_local', 'duration']
DB_GPS_PLUGIN_METADATA_HEADERS = ['ss_gps_lat', 'ss_gps_lon', 'ss_location', 'ss_sog', 'ss_cog', 'ss_distance_from_last_entry', 'ss_cumulative_distance']
DB_GPS_PLUGIN_SUMMARY_HEADERS = ['ss_start_location', 'ss_end_location', 'ss_start_gps_lat', 'ss_start_gps_lon', 'ss_end_gps_lat', 'ss_end_gps_lon', 'ss_distance', 'ss_heading', 'ss_avg_sog']
DB_NMEA_PLUGIN_METADATA_HEADERS = ['nm_true_hdg', 'nm_tws', 'nm_twd', 'nm_aws', 'nm_awa', 'nm_gps_lat', 'nm_gps_lon', 'nm_water_temperature', 'nm_depth', 'nm_sog', 'nm_sow', 'nm_distance_from_last_entry', 'nm_cumulative_distance']
DB_NMEA_PLUGIN_SUMMARY_HEADERS = ['nm_start_location', 'nm_end_location', 'nm_start_gps_lat', 'nm_start_gps_lon', 'nm_end_gps_lat', 'nm_end_gps_lon', 'nm_distance', 'nm_heading', 'nm_avg_wind_speed', 'nm_avg_wind_direction', 'nm_avg_water_temperature', 'nm_avg_depth', 'nm_avg_sog', 'nm_avg_sow']
DB_VICTRON_PLUGIN_METADATA_HEADERS = ['gx_active_input_source', 'gx_grid1_power', 'gx_generator1_power', 'gx_ac_input1_voltage', 'gx_ac_input1_current', 'gx_ac_input1_frequency', 'gx_ve_bus_state', 'gx_ac_consumption', 'gx_batt_voltage', 'gx_batt_current', 'gx_batt_power', 'gx_batt_soc', 'gx_batt_state', 'gx_pv_power', 'gx_pv_current', 'gx_start_batt_voltage', 'gx_tank1_level', 'gx_tank1_type', 'gx_tank2_level', 'gx_tank2_type']
DB_VICTRON_PLUGINS_SUMMARY_HEADERS = ['gx_batt_max_voltage', 'gx_batt_min_voltage', 'gx_batt_avg_voltage', 'gx_batt_max_current', 'gx_batt_avg_current', 'gx_batt_max_power', 'gx_batt_avg_power', 'gx_pv_max_power', 'gx_pv_avg_power', 'gx_pv_max_current', 'gx_pv_avg_current', 'gx_start_batt_max_voltage', 'gx_start_batt_min_voltage', 'gx_start_batt_avg_voltage', 'gx_ac_consumption_max', 'gx_ac_consumption_avg', 'gx_tank1_max_level', 'gx_tank1_min_level', 'gx_tank1_avg_level', 'gx_tank2_max_level', 'gx_tank2_min_level', 'gx_tank2_avg_level']