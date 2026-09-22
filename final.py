import streamlit as st
import math

# ==========================================
# 1. PAGE CONFIGURATION & GLOBAL STYLING
# ==========================================
st.set_page_config(page_title="Blood Bank Refrigerator Design", layout="wide", page_icon="🩸")

st.markdown("""
    <style>
        /* Import Premium Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Apply Font Globally */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* 1. Crisp Premium Light Background Gradient */
        .stApp {
            background: radial-gradient(circle at 10% 20%, rgb(248, 250, 252) 0%, rgb(226, 232, 240) 100%) !important;
        }
        
        /* Global Text Elements */
        p, li, [data-testid="stMarkdownContainer"] p, div[data-testid="stText"] {
            color: #334155 !important;
            font-size: 14px !important; 
        }
        
        /* Clean Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }

        /* Number Input specific styling (Yellow input feel) */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(0, 0, 0, 0.15) !important;
            border-radius: 6px !important;
        }
        
        div[data-baseweb="input"] input {
            color: #0f172a !important;
            font-size: 14px !important; 
            font-weight: 600 !important;
        }
        
        div[data-baseweb="input"]:focus-within {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 1px #3b82f6 !important;
        }

        /* Metric Cards for Outputs */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(0, 0, 0, 0.05) !important;
            border-top: 4px solid #10b981 !important; /* Green top border for outputs */
            padding: 15px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
            transition: transform 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.15) !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: #475569 !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 20px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }

        /* Adjust top padding for a cleaner look */
        .block-container {
            padding-top: 2.5rem !important;
        }
        
        /* Horizontal Rule styling */
        hr {
            margin-top: 0.75rem;
            margin-bottom: 0.75rem;
            border-color: rgba(0, 0, 0, 0.1) !important; 
        }
        
        /* Expander Styling */
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02) !important;
        }
        [data-testid="stExpander"] summary {
            font-weight: 700 !important;
            color: #0f172a !important;
            font-size: 16px !important;
        }
        
        /* Custom UI classes */
        .row-text { padding-top: 8px; font-weight: 600; color: #1e293b; }
        .calc-text { padding-top: 8px; font-weight: 700; color: #3b82f6; font-size: 13px;}
        .ref-text { padding-top: 8px; color: #64748b; font-size: 13px !important; }
    </style>
""", unsafe_allow_html=True)

# Helper function to render "Calculated Yellow Cells" beautifully
def calc_box(label, value, unit="", format_str="{:,.4f}"):
    st.markdown(f"<div class='calc-text'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding: 8px 12px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; font-weight: 600; color: #1e293b; font-size: 14px; margin-bottom: 1rem;'>{format_str.format(value)} {unit}</div>", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
defaults = {
    # Dimension Axis
    "w_int": 61.0, "w_ins": 8.0, "w_ext": 0.0,
    "d_int": 52.9, "d_ins": 8.0, "d_ext": 0.0,
    "h_int": 130.0, "h_ins": 8.0, "h_ext": 0.0,
    "k_puf": 0.0216, "t_int": 2.0, "t_ext": 25.0, "cp_load": 3.6,
    "enthalpy_amb": 56.0, "enthalpy_int": 12.8, "rho_air": 1.25,
    "door_spill": 60.0, "door_opens": 10.0,
    "c47_steady_load": 76.2, "c56_cooling_power": 13.65625, "c62_mass_blood": 141.75, "c66_mass_shelves": 24.0, "c67_cp_steel": 0.5,
    "u_glass": 1.4, "frame_l": 1.6, "frame_w": 0.77, "glass_htr": 35.0, "q_inward_pct": 40.0,
    "ashrae_margin": 1.10, "sst": -4.0, "p_coil": 22.2, "t_ain": 4.0, "t_aout": 1.0,
    "cp_air": 1.005, "bypass_pct": 15.0, "safety_margin_flow": 6.0, "u_finned": 32.00,
    
    # Evaporator & Fins
    "core_h_mm": 101.6, "front_l_mm": 508.0, "tgt_vel": 2.38, "fin_density": 8.0, 
    "fin_height_mm": 110.0, "tube_row_deep": 4.0, "tube_row_high": 4.0, 
    "tube_od_m": 0.009525, "fin_thickness_mm": 0.15, "fin_pitch_mm": 3.175, 
    "collor_margin": 0.196, "fin_therm_eff": 76.0, "dyn_visc_air": 1.74e-5, 
    "staggered_factor": 0.886, "fanning_friction": 0.048, "manuf_smooth": 1.58,
    
    # Refrigerant & Frost
    "r134a_op": -4.0, "cond_temp": 45.0, "evap_enthalpy": 165.0, "spec_vol_r134a": 0.078, 
    "parallel_circuits": 2.0, "tube_inner_dia": 8.0, "eff_factor": 50.0, "buoyancy_mult": 2.0, 
    "w_out": 0.012, "w_in": 0.004, "frost_density": 145.0, "rough_fric_factor": 1.6, 
    "tube_blockage_factor": 1.5, "init_ice_temp": -4.0, "melt_point_temp": 0.0, 
    "cp_ice": 2.11, "lf_water": 334.0, "defrost_time_min": 20.0, "therm_defrost_eff": 15.0,
    "pitch_inch": 1.0, "loops_u_bends": 14.0, "liquid_density": 1294.0, "vapour_density": 14.5, 
    "liquid_mass_pct": 22.0, "vapour_mass_pct": 78.0, "minor_losses_bend": 0.2, 
    "two_phase_fric_factor": 0.024, "liquid_density_neg4": 1294.0, "lockhart_const": 4.8, 
    "surf_bound_prop": 0.64,
    
    # Condensor & Compressor Validation
    "evap_op_press": 2.52, "h_suction": 399.8, "h_liquid": 256.4, "cond_press": 11.6,
    "h_discharge": 435.7, "elec_mech_eff": 30.0, "tec_voltage": 230.0, 
    "tec_current": 2.15, "tec_pf": 0.95,
    
    # NEW FINAL CONDENSOR COIL SIZING & HIGH SIDE CHARGE DEFAULTS
    "cond_run_temp": 45.0, "cond_air_in": 25.0, "cond_air_out": 30.0, "cond_u_coeff": 45.0,
    "cond_w_in": 15.0, "cond_h_in": 6.5, "cond_d_in": 3.0, "cond_tube_od": 9.525,
    "cond_tube_id": 8.0, "cond_tube_rows": 3.0, "cond_tube_high": 3.0, "cond_fin_pitch": 14.0,
    "cond_pitch_mm": 25.4, "cond_fin_eff": 90.0, "cond_air_den": 1.18, "cond_cp_air": 1.005,
    "cond_dt_air": 5.0, "cond_turns": 17.0, "cond_rho_desup": 52.4, "cond_rho_condens": 330.0,
    "cond_rho_subcool": 1146.0, "cond_line_len": 1.1, "cond_line_dia": 0.00476,
    "cond_rho_line": 1146.0, "cond_filter_mass": 75.0, "cond_desup_pct": 10.0,
    "cond_condens_pct": 75.0, "cond_subcool_pct": 15.0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def sync(key):
    st.session_state[key] = st.session_state[key + "_w"]


# ==========================================
# 3. INTERNAL CALCULATIONS (Processed Backend)
# ==========================================
# Phase 1: Core Thermodynamics
vol_cm3 = st.session_state.w_int * st.session_state.d_int * st.session_state.h_int
vol_m3 = vol_cm3 / 1000000.0
vol_liters = vol_m3 * 1000.0
surf_area_cm2 = 2 * ((st.session_state.w_int * st.session_state.d_int) + (st.session_state.w_int * st.session_state.h_int) + (st.session_state.d_int * st.session_state.h_int))
surf_area_m2 = surf_area_cm2 / 10000.0

u_coeff = st.session_state.k_puf / (st.session_state.w_ins / 100.0) if st.session_state.w_ins != 0 else 0.0
delta_t = st.session_state.t_ext - st.session_state.t_int
trans_heat_load = u_coeff * surf_area_m2 * delta_t

delta_h = st.session_state.enthalpy_amb - st.session_state.enthalpy_int
vol_exch_L = vol_liters * (st.session_state.door_spill / 100.0)
vol_exch_m3 = vol_exch_L / 1000.0
mass_exch = vol_exch_m3 * st.session_state.rho_air
energy_inj = mass_exch * delta_h
energy_inj_10 = st.session_state.door_opens * energy_inj
time_avg_w = energy_inj_10 * 1000.0 / 3600.0

heat_transfer_glass = st.session_state.u_glass * st.session_state.frame_l * st.session_state.frame_w * delta_t
heat_transfer_puf = u_coeff * delta_t * st.session_state.frame_l * st.session_state.frame_w
q_inward_calc = st.session_state.glass_htr * (st.session_state.q_inward_pct / 100.0)
total_heat_load_doors = st.session_state.c47_steady_load - heat_transfer_puf + heat_transfer_glass

e_blood = st.session_state.c62_mass_blood * st.session_state.cp_load * delta_t
e_steel = st.session_state.c66_mass_shelves * st.session_state.c67_cp_steel * delta_t
rapid_6h = ((e_blood + e_steel) / (6 * 3600)) * 1000
rapid_8h = ((e_blood + e_steel) / (8 * 3600)) * 1000

total_actual_peak_load = total_heat_load_doors + st.session_state.c56_cooling_power + rapid_8h
q_design = total_actual_peak_load * st.session_state.ashrae_margin
design_evap_load = q_design
actual_running_peak = design_evap_load

temp_diff_c = st.session_state.t_ain - st.session_state.t_aout
temp_diff_k = temp_diff_c

density_4c = 1.25 
mass_flow_air = (design_evap_load / 1000.0) / (st.session_state.cp_air * temp_diff_k) if temp_diff_k != 0 else 0.0
vol_flow_rate = mass_flow_air / density_4c
vol_flow_adj_s = vol_flow_rate * (1 - (st.session_state.bypass_pct / 100.0))
vol_flow_adj_hr = vol_flow_adj_s * 3600.0
req_mass_flow_hr = vol_flow_adj_hr + (vol_flow_adj_hr * (st.session_state.safety_margin_flow / 100.0))
req_mass_flow_s = req_mass_flow_hr / 3600.0

dt_in = st.session_state.t_ain - st.session_state.sst
dt_out = st.session_state.t_aout - st.session_state.sst
lmtd = ((dt_in - dt_out) / math.log(dt_in / dt_out)) if (dt_in > 0 and dt_out > 0 and dt_in != dt_out) else 0.0
ua_conductance = design_evap_load / lmtd if lmtd != 0 else 0.0
aeff = ua_conductance / st.session_state.u_finned if st.session_state.u_finned != 0 else 0.0

# Phase 2: Evaporator & Coil Calculations
f130 = st.session_state.core_h_mm
f131 = f130 / 1000.0
f132 = f130 / 25.4
f135 = st.session_state.front_l_mm
f136 = f135 / 1000.0
f137 = f135 / 25.4
f139 = f131 * f136
f143 = req_mass_flow_s / f139 if f139 != 0 else 0.0
f144 = st.session_state.fin_density
f145 = f144 * f137
f146 = st.session_state.fin_height_mm
f147 = f146 / 25.4
f148 = st.session_state.tube_row_deep
f149 = st.session_state.tube_row_high
f150 = f148 * f149
f151 = st.session_state.tube_od_m
f152 = st.session_state.fin_thickness_mm
f153 = st.session_state.fin_pitch_mm
f154 = f153 - f152

f156 = 2 * ((f146 / 1000.0) * f131)
f157 = f150 * ((3.142 * (f151 ** 2)) / 4.0)
f158 = f156 - f157
f159 = f145 * f158

f163 = 3.142 * f151 * f150 * f136
f164 = 2 * ((f146 / 1000.0) * f131)
f165 = 2 * f150 * ((3.142 * (f151 ** 2)) / 4.0)
f166 = f164 - f165
f167 = f145 * f166
f168 = st.session_state.collor_margin
f169 = f167 + f163 + f168

f173 = st.session_state.fin_therm_eff
f174 = (f173 / 100.0) * f159 + f163

f178 = st.session_state.dyn_visc_air
f179 = f136 * (f146 / 1000.0)
f180 = f145 * (f152 / 1000.0)
f181 = f136 - f180
f182 = f149 * f151
f183 = st.session_state.staggered_factor
f184 = ((f146 / 1000.0) - f182) * f183
f185 = f181 * f184
f186 = f185 / f179 if f179 != 0 else 0.0

c131 = st.session_state.tgt_vel
f187 = c131 / f186 if f186 != 0 else 0.0
f188 = 2 * (f154 / 1000.0)

f189 = (density_4c * f187 * f188) / f178 if f178 != 0 else 0.0
f190 = st.session_state.fanning_friction
f191 = (2 * f190 * f131 * density_4c * (f187 ** 2)) / f188 if f188 != 0 else 0.0
f192 = st.session_state.manuf_smooth
f193 = f191 / f192 if f192 != 0 else 0.0
f194 = f193 * f192

# Phase 3: Flow rate, Frost, Defrost, Charge, and Pressure Drop
mass_flow_ref_s = (q_design / 1000.0) / st.session_state.evap_enthalpy if st.session_state.evap_enthalpy != 0 else 0.0
mass_flow_ref_hr = mass_flow_ref_s * 3600.0
mass_flow_ref_g_min = (mass_flow_ref_hr * 1000.0) / 60.0
vol_flow_ref_inlet_s = mass_flow_ref_s * st.session_state.spec_vol_r134a
vol_flow_ref_inlet_hr = vol_flow_ref_inlet_s * 3600.0
mass_flow_circuit = mass_flow_ref_s / st.session_state.parallel_circuits if st.session_state.parallel_circuits != 0 else 0.0
tube_cross_section = (3.142 * (st.session_state.tube_inner_dia / 1000.0)**2) / 4.0
mass_vel_g = mass_flow_circuit / tube_cross_section if tube_cross_section != 0 else 0.0

v_open = vol_m3 * (st.session_state.eff_factor / 100.0)
v_air_exchange_hr = v_open * st.session_state.door_opens
v_air_exchange_actual = v_air_exchange_hr * st.session_state.buoyancy_mult
w_out_g = st.session_state.w_out * 1000.0
w_in_g = st.session_state.w_in * 1000.0
delta_w = st.session_state.w_out - st.session_state.w_in
air_mass_per_hr = v_air_exchange_actual * st.session_state.rho_air
frost_mass_gen_hr = air_mass_per_hr * delta_w
v_frost_hr_m3 = frost_mass_gen_hr / st.session_state.frost_density if st.session_state.frost_density != 0 else 0.0
v_frost_hr_cc = v_frost_hr_m3 * 1000000.0
growth_rate_m_hr = v_frost_hr_m3 / f169 if f169 != 0 else 0.0
growth_rate_mm_hr = growth_rate_m_hr * 1000.0
t_frost_critical_fin_gap = f154 / ((f194 / f193)**0.2) if (f193 != 0 and (f194/f193) > 0) else 0.0
total_space_lost = f154 - t_frost_critical_fin_gap
t_critical = total_space_lost / 2.0
surf_roughness = st.session_state.rough_fric_factor * st.session_state.tube_blockage_factor
thickness_critical_actual = surf_roughness * t_critical
time_critical = thickness_critical_actual / growth_rate_mm_hr if growth_rate_mm_hr != 0 else 0.0

accum_frost_mass = frost_mass_gen_hr * time_critical
sensible_heat = accum_frost_mass * st.session_state.cp_ice * (st.session_state.melt_point_temp - st.session_state.init_ice_temp)
latent_heat = accum_frost_mass * st.session_state.lf_water
total_theo_heat = sensible_heat + latent_heat
theo_power_kw = total_theo_heat / (st.session_state.defrost_time_min * 60.0) if st.session_state.defrost_time_min != 0 else 0.0
req_elec_capacity = (theo_power_kw * 1000.0) / (st.session_state.therm_defrost_eff / 100.0) if st.session_state.therm_defrost_eff != 0 else 0.0

total_straight_run = f150 * f136
pitch_m = st.session_state.pitch_inch * 0.0254
centerline_bend_rad = pitch_m / 2.0
arc_length = 3.142 * centerline_bend_rad
total_return_bend = st.session_state.loops_u_bends * arc_length
total_developed_length = total_straight_run + total_return_bend
internal_vol_evap_m3 = total_developed_length * tube_cross_section
internal_vol_evap_cc = internal_vol_evap_m3 * 1000000.0
avg_density_evap = ((st.session_state.liquid_mass_pct / 100.0) * st.session_state.liquid_density) + ((st.session_state.vapour_mass_pct / 100.0) * st.session_state.vapour_density)
evap_ref_mass_kg = internal_vol_evap_m3 * avg_density_evap
evap_ref_mass_g = evap_ref_mass_kg * 1000.0

x_minor_loss = st.session_state.loops_u_bends * st.session_state.minor_losses_bend
total_dev_hyd_circuit = total_straight_run + x_minor_loss
press_drop_ref_kpa_raw = st.session_state.lockhart_const * ((st.session_state.two_phase_fric_factor * (total_dev_hyd_circuit / 2.0) * (mass_vel_g ** 2)) / (2.0 * st.session_state.liquid_density_neg4 * (st.session_state.tube_inner_dia / 1000.0))) if (st.session_state.liquid_density_neg4 != 0 and st.session_state.tube_inner_dia != 0) else 0.0
press_drop_ref_actual_kpa = press_drop_ref_kpa_raw * st.session_state.surf_bound_prop
press_drop_ref_actual_bar = press_drop_ref_actual_kpa / 100.0
press_drop_ref_actual_psi = press_drop_ref_actual_bar * 14.5

# Phase 4: Condensor Design & Tecumseh Validation
eff_cooling_work = st.session_state.h_suction - st.session_state.h_liquid
req_comp_work_1 = st.session_state.h_discharge - st.session_state.h_suction
req_comp_work_2 = req_comp_work_1 / (st.session_state.elec_mech_eff / 100.0) if st.session_state.elec_mech_eff != 0 else 0.0
cop_val = eff_cooling_work / req_comp_work_2 if req_comp_work_2 != 0 else 0.0
comp_elec_watt = q_design / cop_val if cop_val != 0 else 0.0

y_watts = st.session_state.tec_voltage * st.session_state.tec_current * st.session_state.tec_pf

# Phase 5: Condensor Coil Sizing & High Side Charge
q_condensor = q_design + comp_elec_watt
dt1_cond = st.session_state.cond_run_temp - st.session_state.cond_air_in
dt2_cond = st.session_state.cond_run_temp - st.session_state.cond_air_out

if dt1_cond > 0 and dt2_cond > 0 and dt1_cond != dt2_cond:
    lmtd_cond = (dt1_cond - dt2_cond) / math.log(dt1_cond / dt2_cond)
else:
    lmtd_cond = dt1_cond if dt1_cond == dt2_cond else 0.0

cond_a_eff_req = q_condensor / (st.session_state.cond_u_coeff * lmtd_cond) if (st.session_state.cond_u_coeff * lmtd_cond) != 0 else 0.0

cond_w_mm = st.session_state.cond_w_in * 25.4
cond_h_mm = st.session_state.cond_h_in * 25.4
cond_d_mm = st.session_state.cond_d_in * 25.4

cond_num_tubes = st.session_state.cond_tube_rows * st.session_state.cond_tube_high
cond_str_len = cond_num_tubes * cond_w_mm / 1000.0
cond_tube_surf = 3.142 * (st.session_state.cond_tube_od / 1000.0) * cond_str_len

cond_n_fins = st.session_state.cond_w_in * st.session_state.cond_fin_pitch
cond_fin_raw = 2 * ((cond_h_mm / 1000.0) * (cond_d_mm / 1000.0))
cond_tube_holes = 2 * cond_num_tubes * (3.142 * ((st.session_state.cond_tube_od / 1000.0)**2) / 4.0)
cond_fin_net = cond_fin_raw - cond_tube_holes
cond_fin_ext = cond_n_fins * cond_fin_net

cond_a_eff_prov = ((st.session_state.cond_fin_eff / 100.0) * cond_fin_ext) + cond_tube_surf

cond_vol_air_s = (q_condensor / 1000.0) / (st.session_state.cond_air_den * st.session_state.cond_cp_air * st.session_state.cond_dt_air) if (st.session_state.cond_air_den * st.session_state.cond_cp_air * st.session_state.cond_dt_air) != 0 else 0.0
cond_vol_air_hr = cond_vol_air_s * 3600.0

cond_bend_rad = (st.session_state.cond_pitch_mm / 2.0) / 1000.0
cond_ret_bends = st.session_state.cond_turns * 3.142 * cond_bend_rad
cond_tot_len = cond_str_len + cond_ret_bends

cond_int_vol_m3 = ((3.142 * (st.session_state.cond_tube_id / 1000.0)**2) / 4.0) * cond_tot_len
cond_int_vol_cc = cond_int_vol_m3 * 1000000.0

m_desup = cond_int_vol_cc * (st.session_state.cond_desup_pct / 100.0) * (st.session_state.cond_rho_desup / 1000.0)
vol_condens = cond_int_vol_cc * (st.session_state.cond_condens_pct / 100.0)
m_condens = vol_condens * (st.session_state.cond_rho_condens / 1000.0)
vol_subcool = cond_int_vol_cc * (st.session_state.cond_subcool_pct / 100.0)
m_subcool = vol_subcool * (st.session_state.cond_rho_subcool / 1000.0)

v_line_m3 = ((3.142 * (st.session_state.cond_line_dia**2)) / 4.0) * st.session_state.cond_line_len
v_line_cc = v_line_m3 * 1000000.0
m_trans_line = v_line_cc * (st.session_state.cond_rho_line / 1000.0)

m_high_side_tot = m_desup + m_condens + m_subcool + m_trans_line + st.session_state.cond_filter_mass

# ==========================================
# 4. GUI LAYOUT & INPUTS (EXPANDERS)
# ==========================================
st.title("🩸 Blood Bank Refrigerator Model")
st.caption("Click the section headers below to expand and view parameters.")

with st.expander("📐 Dimension Axis", expanded=False):
    h_cols = st.columns([1.5, 1.2, 1.2, 1.5, 2])
    h_cols[0].markdown("**Dimension Axis**")
    h_cols[1].markdown("**Internal Chamber (cm)**")
    h_cols[2].markdown("**Insulation Addition (cm)**")
    h_cols[3].markdown("**Final External Footprint (cm)**")
    h_cols[4].markdown("**Reference (Approx / Ext mm)**")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    w_cols = st.columns([1.5, 1.2, 1.2, 1.5, 2])
    w_cols[0].markdown("<div class='row-text'>Cabinet Width W</div>", unsafe_allow_html=True)
    w_cols[1].number_input("w_int", value=st.session_state.w_int, key="w_int_w", on_change=sync, args=("w_int",), step=0.1, label_visibility="collapsed")
    w_cols[2].number_input("w_ins", value=st.session_state.w_ins, key="w_ins_w", on_change=sync, args=("w_ins",), step=0.1, label_visibility="collapsed")
    w_cols[3].number_input("w_ext", value=st.session_state.w_ext, key="w_ext_w", on_change=sync, args=("w_ext",), step=0.1, label_visibility="collapsed")
    w_cols[4].markdown("<div class='ref-text'>approx 650 mm &nbsp;|&nbsp; <b>770 mm</b></div>", unsafe_allow_html=True)

    d_cols = st.columns([1.5, 1.2, 1.2, 1.5, 2])
    d_cols[0].markdown("<div class='row-text'>Cabinet Depth D</div>", unsafe_allow_html=True)
    d_cols[1].number_input("d_int", value=st.session_state.d_int, key="d_int_w", on_change=sync, args=("d_int",), step=0.1, label_visibility="collapsed")
    d_cols[2].number_input("d_ins", value=st.session_state.d_ins, key="d_ins_w", on_change=sync, args=("d_ins",), step=0.1, label_visibility="collapsed")
    d_cols[3].number_input("d_ext", value=st.session_state.d_ext, key="d_ext_w", on_change=sync, args=("d_ext",), step=0.1, label_visibility="collapsed")
    d_cols[4].markdown("<div class='ref-text'>approx 650 mm &nbsp;|&nbsp; <b>660 mm</b></div>", unsafe_allow_html=True)

    ht_cols = st.columns([1.5, 1.2, 1.2, 1.5, 2])
    ht_cols[0].markdown("<div class='row-text'>Cabinet Height H</div>", unsafe_allow_html=True)
    ht_cols[1].number_input("h_int", value=st.session_state.h_int, key="h_int_w", on_change=sync, args=("h_int",), step=0.1, label_visibility="collapsed")
    ht_cols[2].number_input("h_ins", value=st.session_state.h_ins, key="h_ins_w", on_change=sync, args=("h_ins",), step=0.1, label_visibility="collapsed")
    ht_cols[3].number_input("h_ext", value=st.session_state.h_ext, key="h_ext_w", on_change=sync, args=("h_ext",), step=0.1, label_visibility="collapsed")
    ht_cols[4].markdown("<div class='ref-text'>approx 1180 mm &nbsp;|&nbsp; <b>1200 mm</b></div>", unsafe_allow_html=True)

with st.expander("📊 Area Calculation", expanded=False):
    st.markdown("**Internal Volume Metrics**")
    v_c1, v_c2, v_c3 = st.columns(3)
    v_c1.metric("🟢 Internal Volume (cm³)", f"{vol_cm3:,.0f}")
    v_c2.metric("🟢 Internal Volume (m³)", f"{vol_m3:,.6f}")
    v_c3.metric("🟢 Internal Volume (Liters)", f"{vol_liters:,.3f}")
    st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.markdown("**Internal Surface Area Verification**")
    s_c1, s_c2 = st.columns(2)
    s_c1.metric("🟢 Surface Area (cm²)", f"{surf_area_cm2:,.1f}")
    s_c2.metric("🟢 Surface Area (m²)", f"{surf_area_m2:,.5f}")

with st.expander("🌡️ Transmission Heat Load", expanded=False):
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.number_input("Thermal conductivity of PUF (W/m.k)", value=st.session_state.k_puf, key="k_puf_w", on_change=sync, args=("k_puf",), step=0.0001, format="%.4f")
        st.number_input("Cabinet Interior steady Temp (°C)", value=st.session_state.t_int, key="t_int_w", on_change=sync, args=("t_int",), step=0.1)
        st.number_input("Specific Heat (KJ/kg.K)", value=st.session_state.cp_load, key="cp_load_w", on_change=sync, args=("cp_load",), step=0.1)
    with t_c2:
        calc_box("Overall Heat Transfer Coefficient (U)", u_coeff, "W/m²")
        st.number_input("Outside room Temp (°C)", value=st.session_state.t_ext, key="t_ext_w", on_change=sync, args=("t_ext",), step=0.1)
        calc_box("Temperature Difference (Delta T)", delta_t, "K", "{:,.1f}")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    thl_col, _ = st.columns([1, 1])
    thl_col.metric("🟢 Transmission Heat Load (W)", f"{trans_heat_load:,.8f} W")

with st.expander("🌬️ Air Properties (Psychrometrics)", expanded=False):
    p_c1, p_c2, p_c3 = st.columns(3)
    with p_c1: st.number_input("Ambient Air (25°C, 60%) Enthalpy (KJ/kg)", value=st.session_state.enthalpy_amb, key="enthalpy_amb_w", on_change=sync, args=("enthalpy_amb",), step=0.1)
    with p_c2: st.number_input("Internal Air (2°C, 90% RH) Enthalpy (KJ/kg)", value=st.session_state.enthalpy_int, key="enthalpy_int_w", on_change=sync, args=("enthalpy_int",), step=0.1)
    with p_c3: st.number_input("Average Air Density (kg/m³)", value=st.session_state.rho_air, key="rho_air_w", on_change=sync, args=("rho_air",), step=0.01)

with st.expander("🚪 Model Air Exchange per door openings", expanded=False):
    a_c1, a_c2 = st.columns(2)
    with a_c1: st.number_input("Vertical door opens (% of cold air spill)", value=st.session_state.door_spill, key="door_spill_w", on_change=sync, args=("door_spill",), step=1.0)
    with a_c2: st.number_input("Door Openings (times per hour)", value=st.session_state.door_opens, key="door_opens_w", on_change=sync, args=("door_opens",), step=1.0)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    o_c1, o_c2, o_c3 = st.columns(3)
    o_c1.metric("🟠 Vol Exchanges per Opening (Liters)", f"{vol_exch_L:,.4f} L")
    o_c2.metric("🟢 Energy Injected per Opening (KJ)", f"{energy_inj:,.6f} KJ")
    o_c3.metric("🟢 Time Averaged Wattage (W)", f"{time_avg_w:,.5f} W")

with st.expander("🪟 Glass", expanded=False):
    g_c1, g_c2, g_c3 = st.columns(3)
    with g_c1: st.number_input("overall heat transfer coefficient (U-value) W/m²k", value=st.session_state.u_glass, key="u_glass_w", on_change=sync, args=("u_glass",), step=0.1)
    with g_c2: st.number_input("Frame Length (m)", value=st.session_state.frame_l, key="frame_l_w", on_change=sync, args=("frame_l",), step=0.1)
    with g_c3: st.number_input("Width (m)", value=st.session_state.frame_w, key="frame_w_w", on_change=sync, args=("frame_w",), step=0.1)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    go_c1, _ = st.columns([1, 2])
    go_c1.metric("🟢 Heat Transfer (Watts)", f"{heat_transfer_glass:,.4f} W")

with st.expander("🚪 Puf Door (solid Door)", expanded=False):
    po_c1, _ = st.columns([1, 2])
    po_c1.metric("🟢 Heat Transfer (Watts)", f"{heat_transfer_puf:,.5f} W")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    pd_c1, pd_c2, pd_c3 = st.columns(3)
    with pd_c1: st.number_input("Glass wire heater (Watts)", value=st.session_state.glass_htr, key="glass_htr_w", on_change=sync, args=("glass_htr",), step=1.0)
    with pd_c2: st.number_input("Q inward heat leak radiates hates (%)", value=st.session_state.q_inward_pct, key="q_inward_pct_w", on_change=sync, args=("q_inward_pct",), step=1.0)
    with pd_c3: calc_box("Q inward heat leak radiates hates", q_inward_calc, "W", "{:,.1f}")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    po_c2, _ = st.columns([1, 2])
    po_c2.metric("🟢 Total heat load by glass door and PUP box (Watts)", f"{total_heat_load_doors:,.2f} W")

with st.expander("⚡ Total Energy to be removed", expanded=False):
    eo_c1, eo_c2, eo_c3, eo_c4 = st.columns(4)
    eo_c1.metric("🟢 Blood Energy Removal E blood (KJ)", f"{e_blood:,.1f} KJ")
    eo_c2.metric("🟢 G steel Crated Energy Removall", f"{e_steel:,.0f} KJ") 
    eo_c3.metric("🟢 Scenariao A 6 hours Rapid full down (W)", f"{rapid_6h:,.5f} W")
    eo_c4.metric("🟢 Scenariao A 8 hours Rapid full down (W)", f"{rapid_8h:,.5f} W")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    po_c1, po_c2 = st.columns(2)
    with po_c1: po_c1.metric("🟢 Total Actual Running Peak Load (W)", f"{total_actual_peak_load:,.0f} W")
    with po_c2: st.number_input("Ashre Guidelines Mandate (10% to 15% safety factor)", value=st.session_state.ashrae_margin, key="ashrae_margin_w", on_change=sync, args=("ashrae_margin",), step=0.01)
    po_c3, po_c4 = st.columns(2)
    po_c3.metric("🟢 Q design (W)", f"{q_design:,.2f} W")
    po_c4.metric("🟢 Design Evaporator Running at Peak Load (W)", f"{design_evap_load:,.2f} W")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    tp_c1, tp_c2 = st.columns(2)
    with tp_c1:
        calc_box("The actual Running Peak Load", actual_running_peak, "W", "{:,.0f}")
        st.number_input("Saturated Suction Temperature (SST) °C", value=st.session_state.sst, key="sst_w", on_change=sync, args=("sst",), step=1.0)
        st.number_input("Coil Pressure (R134a) psi", value=st.session_state.p_coil, key="p_coil_w", on_change=sync, args=("p_coil",), step=0.1)
    with tp_c2:
        st.number_input("Air Inlet Temperature (T a,in) °C", value=st.session_state.t_ain, key="t_ain_w", on_change=sync, args=("t_ain",), step=1.0)
        st.number_input("Air outlet temperature from coil °C", value=st.session_state.t_aout, key="t_aout_w", on_change=sync, args=("t_aout",), step=1.0)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    td_c1, td_c2 = st.columns(2)
    td_c1.metric("🟢 Temperature difference (°C)", f"{temp_diff_c:.0f} C")
    td_c2.metric("🟢 Temperature difference (K)", f"{temp_diff_k:.0f} K")

with st.expander("💨 Calculate the required Air mass flow rate", expanded=False):
    amf_c1, amf_c2, amf_c3 = st.columns(3)
    with amf_c1:
        st.number_input("Cp of the air (KJ/kg.K)", value=st.session_state.cp_air, key="cp_air_w", on_change=sync, args=("cp_air",), step=0.001, format="%.3f")
        st.number_input("To compensate by pass (%)", value=st.session_state.bypass_pct, key="bypass_pct_w", on_change=sync, args=("bypass_pct",), step=1.0)
    with amf_c2:
        st.number_input("6% safty margin flow (%)", value=st.session_state.safety_margin_flow, key="safety_margin_flow_w", on_change=sync, args=("safety_margin_flow",), step=1.0)
    with amf_c3:
        st.info("Bypass factor 85% air hits target temperature 15% by pass it To compensate", icon="ℹ️")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    m_c1, m_c2, m_c3 = st.columns(3)
    m_c1.metric("🟢 mass flow air (kg/s)", f"{mass_flow_air:,.8f} kg/s")
    m_c2.metric("🟠 Density of air at 4°C (kg/s)", f"{density_4c:,.2f} kg/s")
    m_c3.metric("🟢 Volume flow rate (m³/s)", f"{vol_flow_rate:,.8f} m³/s")
    st.markdown("<br>", unsafe_allow_html=True)
    a_c1, a_c2, a_c3, a_c4 = st.columns(4)
    a_c1.metric("🟢 Volume flow rate (adjusted) (m³/s)", f"{vol_flow_adj_s:,.8f} m³/s")
    a_c2.metric("🟢 Volume flow rate (adjusted) (m³/hr)", f"{vol_flow_adj_hr:,.7f} m³/hr")
    a_c3.metric("🟢 Required mass flow (m³/hr)", f"{req_mass_flow_hr:,.7f} m³/hr")
    a_c4.metric("🟢 Required mass flow (m³/s)", f"{req_mass_flow_s:,.8f} m³/s")

with st.expander("🌡️ Log Mean Temperature Difference (LMTD)", expanded=False):
    lm_c1, lm_c2 = st.columns(2)
    with lm_c1:
        calc_box("Air Temperature IN - SST", dt_in, "K", "{:,.1f}")
        calc_box("Air Temperature OUT - SST", dt_out, "K", "{:,.1f}")
    with lm_c2:
        st.number_input("Overall Heat Transfer Coefficient (U) fiined matrix (W/m²K)", value=st.session_state.u_finned, key="u_finned_w", on_change=sync, args=("u_finned",), step=0.1)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    l_c1, l_c2, l_c3 = st.columns(3)
    l_c1.metric("🟢 LMTD (K)", f"{lmtd:,.2f} K")
    l_c2.metric("🟢 Thermal Conductance (UA) (W/K)", f"{ua_conductance:,.2f} W/K")
    l_c3.metric("🟢 Aeff (m²)", f"{aeff:,.2f} m²")

with st.expander("📏 Evaporator Dimensions", expanded=False):
    ev1_c1, ev1_c2, ev1_c3 = st.columns(3)
    with ev1_c1:
        st.number_input("Core Height (mm)", value=st.session_state.core_h_mm, key="core_h_mm_w", on_change=sync, args=("core_h_mm",), step=1.0)
        st.number_input("Frontal Length (mm)", value=st.session_state.front_l_mm, key="front_l_mm_w", on_change=sync, args=("front_l_mm",), step=1.0)
        st.number_input("Target face velocity (m/s)", value=st.session_state.tgt_vel, key="tgt_vel_w", on_change=sync, args=("tgt_vel",), step=0.1)
    with ev1_c2:
        st.number_input("fin density (FPI)", value=st.session_state.fin_density, key="fin_density_w", on_change=sync, args=("fin_density",), step=1.0)
        st.number_input("Fin Height (mm)", value=st.session_state.fin_height_mm, key="fin_height_mm_w", on_change=sync, args=("fin_height_mm",), step=1.0)
        st.number_input("number of tube row in deep", value=st.session_state.tube_row_deep, key="tube_row_deep_w", on_change=sync, args=("tube_row_deep",), step=1.0)
    with ev1_c3:
        st.number_input("Number of Tubes in high", value=st.session_state.tube_row_high, key="tube_row_high_w", on_change=sync, args=("tube_row_high",), step=1.0)
        st.number_input("Tube outer diameter (3/8) (m)", value=st.session_state.tube_od_m, key="tube_od_m_w", on_change=sync, args=("tube_od_m",), step=0.0001, format="%.6f")
        st.number_input("Fin Thickness (mm)", value=st.session_state.fin_thickness_mm, key="fin_thickness_mm_w", on_change=sync, args=("fin_thickness_mm",), step=0.01)
        st.number_input("Fins pitch spacing :8FPI (mm)", value=st.session_state.fin_pitch_mm, key="fin_pitch_mm_w", on_change=sync, args=("fin_pitch_mm",), step=0.01)

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    calc_c1, calc_c2, calc_c3 = st.columns(3)
    with calc_c1: calc_box("Number of fins", f145, "fins", "{:,.0f}")
    with calc_c2: calc_box("Total tubes", f150, "", "{:,.0f}")
    with calc_c3: calc_box("Clear air gap spcing", f154, "mm")
    st.markdown("<br>", unsafe_allow_html=True)
    o1_c1, o1_c2 = st.columns(2)
    o1_c1.metric("🟢 Calculate the frontal area (m²)", f"{f139:,.7f} m²")
    o1_c2.metric("🟢 Velocity at front Face (m/s)", f"{f143:,.8f} m/s")

with st.expander("📐 Calculate Secondary surface area of Fins", expanded=False):
    sec_c1, sec_c2 = st.columns(2)
    with sec_c1:
        calc_box("Area of one Fin sheet", f156, "m²")
        calc_box("Substract the Tube Holes from one fin", f157, "m²", "{:,.7f}")
    with sec_c2:
        calc_box("Net Area of per fin", f158, "m²", "{:,.8f}")
        calc_box("Total Net of all fins", f159, "m²")

with st.expander("🧮 Calcuate primary surface area of the tubes", expanded=False):
    pri_c1, pri_c2 = st.columns(2)
    with pri_c1:
        calc_box("Total outer Tube surface area", f163, "m²", "{:,.8f}")
        calc_box("Surface area of Fins (Afins)", f164, "m²")
        calc_box("Area of 16 holes (both sides)", f165, "m²", "{:,.8f}")
    with pri_c2:
        calc_box("Net area of one Single Fin sheet", f166, "m²", "{:,.8f}")
        calc_box("Net total fin surface 160 sheet", f167, "m²", "{:,.7f}")
        st.number_input("Collor margin (m²)", value=st.session_state.collor_margin, key="collor_margin_w", on_change=sync, args=("collor_margin",), step=0.01)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    calc_box("Total Raw Area", f169, "m²")

with st.expander("✨ Total Effective area of the fin", expanded=False):
    eff_c1, eff_c2 = st.columns(2)
    with eff_c1: st.number_input("Fin thermal Effciency (%)", value=st.session_state.fin_therm_eff, key="fin_therm_eff_w", on_change=sync, args=("fin_therm_eff",), step=1.0)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.metric("🟢 Aeff (m²)", f"{f174:,.8f} m²")

with st.expander("💨 Air Pressure Drop", expanded=False):
    ap_c1, ap_c2 = st.columns(2)
    with ap_c1:
        st.number_input("Dynamic Viscosity of air (Pa.s)", value=st.session_state.dyn_visc_air, key="dyn_visc_air_w", on_change=sync, args=("dyn_visc_air",), step=1e-6, format="%.2e")
        st.number_input("Staggered factor", value=st.session_state.staggered_factor, key="staggered_factor_w", on_change=sync, args=("staggered_factor",), step=0.01)
    with ap_c2:
        st.number_input("Fanning Friction factor", value=st.session_state.fanning_friction, key="fanning_friction_w", on_change=sync, args=("fanning_friction",), step=0.001, format="%.3f")
        st.number_input("Manufacture smoothing reduce by", value=st.session_state.manuf_smooth, key="manuf_smooth_w", on_change=sync, args=("manuf_smooth",), step=0.01)
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    cb_c1, cb_c2, cb_c3 = st.columns(3)
    with cb_c1:
        calc_box("Aface", f179, "m²", "{:,.4f}")
        calc_box("Number of tube blockage", f182, "m", "{:,.4f}")
        calc_box("Final Ratio (kays and London)", f186, "", "{:,.8f}")
    with cb_c2:
        calc_box("Total fin Blockage", f180, "m", "{:,.3f}")
        calc_box("Effective open Height Path", f184, "m", "{:,.6f}")
        calc_box("Vmax", f187, "m/s", "{:,.8f}")
    with cb_c3:
        calc_box("Net open Width", f181, "m", "{:,.3f}")
        calc_box("Amin", f185, "m²", "{:,.8f}")
        calc_box("Hydraulic Diameter at narrow spacing", f188, "m", "{:,.5f}")
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    res_c1, res_c2 = st.columns(2)
    res_c1.metric("🟢 Reynolds Number", f"{f189:,.2e}")
    res_c1.metric("🟢 Dry air Pressure drop inside Evaporator (Pa)", f"{f193:,.8f} Pa")
    res_c2.metric("🟢 Pressure drop (dry) (Pa)", f"{f191:,.8f} Pa")
    res_c2.metric("🟢 Pressure drop at wet (Pa)", f"{f194:,.8f} Pa")

with st.expander("🌊 Flow rate of the refrigerant", expanded=False):
    fr_c1, fr_c2 = st.columns(2)
    with fr_c1:
        st.number_input("For R134a Operating (°C)", value=st.session_state.r134a_op, key="r134a_op_w", on_change=sync, args=("r134a_op",), step=1.0)
        st.number_input("condensing Temperature (°C)", value=st.session_state.cond_temp, key="cond_temp_w", on_change=sync, args=("cond_temp",), step=1.0)
        st.number_input("Evapoarator Enathalpy (KJ/Kg)", value=st.session_state.evap_enthalpy, key="evap_enthalpy_w", on_change=sync, args=("evap_enthalpy",), step=1.0)
    with fr_c2:
        st.number_input("Specific Volume R134a (m³/m)", value=st.session_state.spec_vol_r134a, key="spec_vol_r134a_w", on_change=sync, args=("spec_vol_r134a",), step=0.001, format="%.3f")
        calc_box("Volumetric Flow Rate at Compressor inlet (m³/s)", vol_flow_ref_inlet_s, "m³/s", "{:,.8f}")
        calc_box("Volumetric Flow Rate at Compressor inlet (m³/hr)", vol_flow_ref_inlet_hr, "m³/hr", "{:,.8f}")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    fr2_c1, fr2_c2 = st.columns(2)
    with fr2_c1:
        st.number_input("Number of parallel Feed cicrcuit", value=st.session_state.parallel_circuits, key="parallel_circuits_w", on_change=sync, args=("parallel_circuits",), step=1.0)
    with fr2_c2:
        st.number_input("Tube Inner diamter (mm)", value=st.session_state.tube_inner_dia, key="tube_inner_dia_w", on_change=sync, args=("tube_inner_dia",), step=1.0)

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    fr3_c1, fr3_c2, fr3_c3 = st.columns(3)
    fr3_c1.metric("🟢 Mass flow rate (kg/s)", f"{mass_flow_ref_s:,.8f} kg/s")
    fr3_c2.metric("🟢 Mass flow rate (kg/hr)", f"{mass_flow_ref_hr:,.8f} kg/hr")
    fr3_c3.metric("🟢 Mass flow rate (grams/minute)", f"{mass_flow_ref_g_min:,.8f} g/m")
    
    fr4_c1, fr4_c2 = st.columns(2)
    fr4_c1.metric("🟢 mass flow rate per circuit (kg/s)", f"{mass_flow_circuit:,.8f} kg/s")
    fr4_c2.metric("🟢 Mass Velocity (G) (kg/m².S)", f"{mass_vel_g:,.8f} kg/m².S")

with st.expander("❄️ Frost Formation", expanded=False):
    ff_c1, ff_c2 = st.columns(2)
    with ff_c1:
        st.number_input("Effectiveness Factor (E_x) of exactly 0.50 (%)", value=st.session_state.eff_factor, key="eff_factor_w", on_change=sync, args=("eff_factor",), step=1.0)
        calc_box("Vopen (m³ per door opening)", v_open, "m³", "{:,.6f}")
        calc_box("Calculate the Hourly Air Infiltration Volume (Vair exchange)", v_air_exchange_hr, "m³/hr", "{:,.6f}")
    with ff_c2:
        st.number_input("Bouyancy Height Multiplier", value=st.session_state.buoyancy_mult, key="buoyancy_mult_w", on_change=sync, args=("buoyancy_mult",), step=1.0)
        calc_box("V air exchange actual (m³/hr)", v_air_exchange_actual, "m³/hr", "{:,.5f}")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    ff2_c1, ff2_c2 = st.columns(2)
    with ff2_c1:
        st.number_input("ω_out (kg/kg)", value=st.session_state.w_out, key="w_out_w", on_change=sync, args=("w_out",), step=0.001, format="%.3f")
        calc_box("ω_out (grams of water per kilogran dry air)", w_out_g, "g/kg")
        st.number_input("ω_in Inside cabinet air (2°C ,90%RH) (kg/kg)", value=st.session_state.w_in, key="w_in_w", on_change=sync, args=("w_in",), step=0.001, format="%.3f")
        calc_box("ω_in (grams of water per kilogran dry air)", w_in_g, "g/kg")
    with ff2_c2:
        calc_box("Moisture Removed per air change (Delta w)", delta_w, "kg/kg", "{:,.3f}")
        calc_box("Air mass per hour (kg/h)", air_mass_per_hr, "kg/h", "{:,.6f}")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    ff3_c1, ff3_c2 = st.columns(2)
    with ff3_c1:
        st.metric("🟢 Total hourly Frost Mass generationb(mfrost)", f"{frost_mass_gen_hr:,.7f} kg/h")
        st.number_input("Frost density (kg/m³)", value=st.session_state.frost_density, key="frost_density_w", on_change=sync, args=("frost_density",), step=1.0)
        calc_box("Vfrost per hour (m³/hr)", v_frost_hr_m3, "m³/hr", "{:,.8f}")
        calc_box("Vfrost per hour (cc/hr)", v_frost_hr_cc, "cc/hr", "{:,.6f}")
        calc_box("Growth Rate (m/hour)", growth_rate_m_hr, "m/hour", "{:,.2e}")
        calc_box("Growth Rate (mm/hour)", growth_rate_mm_hr, "mm/hour", "{:,.8f}")
    with ff3_c2:
        calc_box("Crtical Constructed Fin Gap (t frost) (mm)", t_frost_critical_fin_gap, "mm", "{:,.8f}")
        calc_box("Total space lost (mm)", total_space_lost, "mm", "{:,.8f}")
        calc_box("t critical (mm)", t_critical, "mm", "{:,.8f}")
        st.number_input("Roughness Friction Factor", value=st.session_state.rough_fric_factor, key="rough_fric_factor_w", on_change=sync, args=("rough_fric_factor",), step=0.1)
        st.number_input("Tube blockage", value=st.session_state.tube_blockage_factor, key="tube_blockage_factor_w", on_change=sync, args=("tube_blockage_factor",), step=0.1)
        calc_box("Surafce Rougfness", surf_roughness, "", "{:,.2f}")
        calc_box("Thickness critical Actual (mm)", thickness_critical_actual, "mm", "{:,.8f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("🟢 Time (critical) (hours)", f"{time_critical:,.8f} hours")

with st.expander("⚡ Defrost Electrical Heat Capacity", expanded=False):
    de_c1, de_c2 = st.columns(2)
    with de_c1:
        calc_box("Accoumulation of frost Mass(mfrost) (kg)", accum_frost_mass, "kg", "{:,.8f}")
        st.number_input("Intial Ice Temperature (°C)", value=st.session_state.init_ice_temp, key="init_ice_temp_w", on_change=sync, args=("init_ice_temp",), step=1.0)
        st.number_input("Melting Point Temperature (°C)", value=st.session_state.melt_point_temp, key="melt_point_temp_w", on_change=sync, args=("melt_point_temp",), step=1.0)
        st.number_input("Specific Heat of Ice(cp ice) (KJ/kg.K)", value=st.session_state.cp_ice, key="cp_ice_w", on_change=sync, args=("cp_ice",), step=0.01)
    with de_c2:
        st.number_input("Latent Heat of Fusion of water (lf) (KJ/kg.K)", value=st.session_state.lf_water, key="lf_water_w", on_change=sync, args=("lf_water",), step=1.0)
        calc_box("Senisble Heat Phase (warming the ice from -4°C to 0°C)", sensible_heat, "KJ", "{:,.8f}")
        calc_box("Latent Heat Phase", latent_heat, "KJ", "{:,.6f}")
        calc_box("Total Theroretical Heat required", total_theo_heat, "KJ", "{:,.8f}")
        
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    de2_c1, de2_c2 = st.columns(2)
    with de2_c1:
        st.number_input("20 mintutes defrost timeline (min)", value=st.session_state.defrost_time_min, key="defrost_time_min_w", on_change=sync, args=("defrost_time_min",), step=1.0)
        calc_box("Theeoretical Power (KW)", theo_power_kw, "KW", "{:,.8f}")
        st.number_input("Thermal defrost Efficiency (%)", value=st.session_state.therm_defrost_eff, key="therm_defrost_eff_w", on_change=sync, args=("therm_defrost_eff",), step=1.0)
    with de2_c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.metric("🟢 Required Electrical Capacity (Watts)", f"{req_elec_capacity:,.6f} Watts")

with st.expander("🔋 Charge calculation", expanded=False):
    cc_c1, cc_c2 = st.columns(2)
    with cc_c1:
        calc_box("Total staright run of the tube (m)", total_straight_run, "m", "{:,.3f}")
        st.number_input("Pitch (inch)", value=st.session_state.pitch_inch, key="pitch_inch_w", on_change=sync, args=("pitch_inch",), step=0.1)
        calc_box("Centerline Bend radious (m)", centerline_bend_rad, "m", "{:,.4f}")
        calc_box("Arc Length of a single 180°Bend (m)", arc_length, "m", "{:,.6f}")
    with cc_c2:
        st.number_input("loops U bends", value=st.session_state.loops_u_bends, key="loops_u_bends_w", on_change=sync, args=("loops_u_bends",), step=1.0)
        calc_box("Total Return Bend Length (m)", total_return_bend, "m", "{:,.6f}")
        calc_box("Total Developed Length (m)", total_developed_length, "m", "{:,.6f}")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    cc2_c1, cc2_c2 = st.columns(2)
    cc2_c1.metric("🟢 Internal Volume (m³)", f"{internal_vol_evap_m3:,.8f} m³")
    cc2_c2.metric("🟢 Internal Volume (CC)", f"{internal_vol_evap_cc:,.6f} CC")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    cc3_c1, cc3_c2 = st.columns(2)
    with cc3_c1:
        st.number_input("Liquid density (kg/m³)", value=st.session_state.liquid_density, key="liquid_density_w", on_change=sync, args=("liquid_density",), step=1.0)
        st.number_input("Vapour density (kg/m³)", value=st.session_state.vapour_density, key="vapour_density_w", on_change=sync, args=("vapour_density",), step=0.1)
        st.number_input("Liquid mass percenatge (%)", value=st.session_state.liquid_mass_pct, key="liquid_mass_pct_w", on_change=sync, args=("liquid_mass_pct",), step=1.0)
    with cc3_c2:
        st.number_input("Vapour percenatge (%)", value=st.session_state.vapour_mass_pct, key="vapour_mass_pct_w", on_change=sync, args=("vapour_mass_pct",), step=1.0)
        calc_box("Average density of Evp (kg/m³)", avg_density_evap, "kg/m³", "{:,.2f}")
        
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    cc4_c1, cc4_c2 = st.columns(2)
    cc4_c1.metric("🟢 Evap Refrigerant mass (kg)", f"{evap_ref_mass_kg:,.8f} kg")
    cc4_c2.metric("🟢 Evap Refrigerant mass (grams)", f"{evap_ref_mass_g:,.6f} grams")

with st.expander("📉 Pressure drop inside Evaporator", expanded=False):
    pd_c1, pd_c2 = st.columns(2)
    with pd_c1:
        st.number_input("Assuming minor losses of the bend its roughness (m)", value=st.session_state.minor_losses_bend, key="minor_losses_bend_w", on_change=sync, args=("minor_losses_bend",), step=0.1)
        calc_box("x (m)", x_minor_loss, "m", "{:,.1f}")
        calc_box("Total Developed Hydraulic Circuit Length (m)", total_dev_hyd_circuit, "m", "{:,.3f}")
    with pd_c2:
        st.number_input("The integrated two-phase flow resistance uses a liquid-equivalent friction factor (f)", value=st.session_state.two_phase_fric_factor, key="two_phase_fric_factor_w", on_change=sync, args=("two_phase_fric_factor",), step=0.001, format="%.3f")
        st.number_input("Liquid density at -4°C (kg/m³)", value=st.session_state.liquid_density_neg4, key="liquid_density_neg4_w", on_change=sync, args=("liquid_density_neg4",), step=1.0)
        st.number_input("Lockhart Martinelli two phse constant", value=st.session_state.lockhart_const, key="lockhart_const_w", on_change=sync, args=("lockhart_const",), step=0.1)

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.metric("🟢 Pressure drop refrigerant inside Evaporator (kPa)", f"{press_drop_ref_kpa_raw:,.8f} kPa")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    pd2_c1, pd2_c2 = st.columns(2)
    with pd2_c1:
        st.number_input("defining for Internal Surface Boundary Properties:", value=st.session_state.surf_bound_prop, key="surf_bound_prop_w", on_change=sync, args=("surf_bound_prop",), step=0.01)
        st.caption("Because a smooth lubricating oil film forms along the inner walls of the copper tubes, it acts as a micro-hydraulic cushion. This boundary layer reduction drops the raw shear friction by roughly 35%, settling your true operating pressure drop at its final targeted engineering parameter.")
    with pd2_c2:
        st.metric("🟢 Pressure Drop refrigernant actual (kPa)", f"{press_drop_ref_actual_kpa:,.8f} kPa")
        st.metric("🟢 Pressure Drop refrigernant actual (bar)", f"{press_drop_ref_actual_bar:,.8f} bar")
        st.metric("🟢 Pressure Drop refrigernant actual (psi)", f"{press_drop_ref_actual_psi:,.8f} psi")

# ------------------------------------------
# EXPANDER 21: Condensor Thermodynamics & Compressor Work
# ------------------------------------------
with st.expander("⚙️ Condensor Thermodynamics & Compressor Work", expanded=False):
    st.caption("Evaporating at -4°C (2.52 bar) with a target superheat gas temperature of 4°C entering the suction valve.")
    st.caption("High-Pressure Side (Condenser): Condensing at 45°C (11.60 bar) with a liquid subcooling point of 40°C entering the capillary tube")
    st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    cd_c1, cd_c2 = st.columns(2)
    with cd_c1:
        st.number_input("Evpoarator operating pressure at -4°C (bar)", value=st.session_state.evap_op_press, key="evap_op_press_w", on_change=sync, args=("evap_op_press",), step=0.1)
        st.number_input("Enthalpy of Suction Gas (hsuction) (Kj/Kg)", value=st.session_state.h_suction, key="h_suction_w", on_change=sync, args=("h_suction",), step=0.1)
        st.number_input("Enthalpy of Liquid (h_liquid) (Kj/Kg)", value=st.session_state.h_liquid, key="h_liquid_w", on_change=sync, args=("h_liquid",), step=0.1)
        st.number_input("Condensing Pressure (bar)", value=st.session_state.cond_press, key="cond_press_w", on_change=sync, args=("cond_press",), step=0.1)
    with cd_c2:
        st.number_input("Enthalpy of Discharge Gas (h_discharge) (Kj/Kg)", value=st.session_state.h_discharge, key="h_discharge_w", on_change=sync, args=("h_discharge",), step=0.1)
        calc_box("Calculate the Effective Cooling Work", eff_cooling_work, "Kj/Kg", "{:,.1f}")
        calc_box("calculate the Required Compressor Compression Work", req_comp_work_1, "Kj/Kg", "{:,.1f}")
        st.number_input("Overall electromechanical effciency (%)", value=st.session_state.elec_mech_eff, key="elec_mech_eff_w", on_change=sync, args=("elec_mech_eff",), step=1.0)
        calc_box("calculate the Required Compressor Compression Work", req_comp_work_2, "KJ/Kg", "{:,.8f}")

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    cd2_c1, cd2_c2 = st.columns(2)
    cd2_c1.metric("🟢 COP", f"{cop_val:,.8f}")
    cd2_c2.metric("🟢 Compressor Electrical watt", f"{comp_elec_watt:,.8f} Watts")

with st.expander("📋 Cross-Checking with Your Selected Tecumseh Datasheet", expanded=False):
    st.markdown("**Nomainal Power draw**")
    tc_c1, tc_c2, tc_c3 = st.columns(3)
    with tc_c1:
        st.number_input("Voltage (V)", value=st.session_state.tec_voltage, key="tec_voltage_w", on_change=sync, args=("tec_voltage",), step=1.0)
    with tc_c2:
        st.number_input("Current (A)", value=st.session_state.tec_current, key="tec_current_w", on_change=sync, args=("tec_current",), step=0.1)
    with tc_c3:
        st.number_input("Power Factor (PF)", value=st.session_state.tec_pf, key="tec_pf_w", on_change=sync, args=("tec_pf",), step=0.01)

    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    tc2_c1, _ = st.columns([1, 2])
    tc2_c1.metric("🟢 y (Watts)", f"{y_watts:,.3f} Watts")

# ------------------------------------------
# EXPANDER 23: Condensor Coil Sizing & High Side Charge
# ------------------------------------------
with st.expander("🌀 Condensor Coil Sizing & High Side Charge", expanded=True):
    # Heat Load & LMTD
    st.markdown("### Condensor Heat Load & LMTD")
    cc_h1, cc_h2, cc_h3 = st.columns(3)
    with cc_h1:
        st.number_input("condesor Running at (°C)", value=st.session_state.cond_run_temp, key="cond_run_temp_w", on_change=sync, args=("cond_run_temp",), step=1.0)
        st.number_input("Condensor fan pulls fan air (°C)", value=st.session_state.cond_air_in, key="cond_air_in_w", on_change=sync, args=("cond_air_in",), step=1.0)
        st.number_input("and expell (°C)", value=st.session_state.cond_air_out, key="cond_air_out_w", on_change=sync, args=("cond_air_out",), step=1.0)
    with cc_h2:
        st.number_input("Overall Heat trasfer coefficent U (W/m²K)", value=st.session_state.cond_u_coeff, key="cond_u_coeff_w", on_change=sync, args=("cond_u_coeff",), step=1.0)
        calc_box("LMTD (K)", lmtd_cond, "K", "{:,.8f}")
    with cc_h3:
        st.metric("🟢 Qcondensor (Watts)", f"{q_condensor:,.2f} W")
        st.metric("🟢 Aeffective (m²)", f"{cond_a_eff_req:,.8f} m²")

    st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # Coil Dimensions
    st.markdown("### Dimension & Tube Details")
    cc_d1, cc_d2, cc_d3 = st.columns(3)
    with cc_d1:
        st.number_input("Width (inch)", value=st.session_state.cond_w_in, key="cond_w_in_w", on_change=sync, args=("cond_w_in",), step=1.0)
        st.number_input("Height (inch)", value=st.session_state.cond_h_in, key="cond_h_in_w", on_change=sync, args=("cond_h_in",), step=0.1)
        st.number_input("Depth (inch)", value=st.session_state.cond_d_in, key="cond_d_in_w", on_change=sync, args=("cond_d_in",), step=0.1)
        calc_box("Width (mm)", cond_w_mm, "mm", "{:,.1f}")
        calc_box("Height (mm)", cond_h_mm, "mm", "{:,.1f}")
        calc_box("Depth (mm)", cond_d_mm, "mm", "{:,.1f}")
    with cc_d2:
        st.number_input("Tube outer diameter (3/8)\" (mm)", value=st.session_state.cond_tube_od, key="cond_tube_od_w", on_change=sync, args=("cond_tube_od",), step=0.001, format="%.3f")
        st.number_input("Tube inner dimater (mm)", value=st.session_state.cond_tube_id, key="cond_tube_id_w", on_change=sync, args=("cond_tube_id",), step=0.1)
        st.number_input("Number of tube rows", value=st.session_state.cond_tube_rows, key="cond_tube_rows_w", on_change=sync, args=("cond_tube_rows",), step=1.0)
        st.number_input("Number of tube in high side", value=st.session_state.cond_tube_high, key="cond_tube_high_w", on_change=sync, args=("cond_tube_high",), step=1.0)
        calc_box("Number of tubes", cond_num_tubes, "", "{:,.0f}")
        calc_box("Total straight Length (m)", cond_str_len, "m", "{:,.3f}")
    with cc_d3:
        st.number_input("Fin pitch spacing (FPI)", value=st.session_state.cond_fin_pitch, key="cond_fin_pitch_w", on_change=sync, args=("cond_fin_pitch",), step=1.0)
        st.number_input("Pitch (mm)", value=st.session_state.cond_pitch_mm, key="cond_pitch_mm_w", on_change=sync, args=("cond_pitch_mm",), step=0.1)
        st.number_input("Fin Thermal Efficiency Factor (nf) (%)", value=st.session_state.cond_fin_eff, key="cond_fin_eff_w", on_change=sync, args=("cond_fin_eff",), step=1.0)
        calc_box("Coper Tube Surafce Area (Atubes)", cond_tube_surf, "m²", "{:,.8f}")
        calc_box("Total number of fin plates (Nfins)", cond_n_fins, "Fins", "{:,.0f}")
    
    st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    fin_c1, fin_c2 = st.columns(2)
    with fin_c1:
        calc_box("Raw Face Area of one fne sheet (both sides) (Afin raw)", cond_fin_raw, "m²", "{:,.8f}")
        calc_box("Subtrcat 9 punched tube Holes (both side)", cond_tube_holes, "m²", "{:,.8f}")
    with fin_c2:
        calc_box("Net Surface Area per Fin sheet", cond_fin_net, "m²", "{:,.8f}")
        calc_box("Total Extended Fin surface area", cond_fin_ext, "m²", "{:,.8f}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("🟢 Area of effective (m²)", f"{cond_a_eff_prov:,.8f} m²")
    st.info("Sizing Reconciliation: The real physical core provides 4.613 m², which heavily exceeds your first-principles requirement of 1.303 m². This large safety factor ensures that even if hospital dust blocks up to 70% of the fin channels over time, the system will still successfully dump the 1.02 kW load without spiking head pressures.")

    st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # Airflow & Bends
    st.markdown("### Airflow & Returns")
    air_c1, air_c2 = st.columns(2)
    with air_c1:
        st.number_input("Density of air (kg/m³)", value=st.session_state.cond_air_den, key="cond_air_den_w", on_change=sync, args=("cond_air_den",), step=0.01)
        st.number_input("Cp (kJ/kg)", value=st.session_state.cond_cp_air, key="cond_cp_air_w", on_change=sync, args=("cond_cp_air",), step=0.001, format="%.3f")
        st.number_input("Temperature Difference (K)", value=st.session_state.cond_dt_air, key="cond_dt_air_w", on_change=sync, args=("cond_dt_air",), step=1.0)
        st.number_input("Number of turns", value=st.session_state.cond_turns, key="cond_turns_w", on_change=sync, args=("cond_turns",), step=1.0)
    with air_c2:
        calc_box("Bend Radious (m)", cond_bend_rad, "m", "{:,.4f}")
        calc_box("Total Return bends length (m)", cond_ret_bends, "m", "{:,.6f}")
        st.metric("🟢 Volumetric air flow rate (m³/s)", f"{cond_vol_air_s:,.8f} m³/s")
        st.metric("🟢 Volumetric air flow rate (m³/hr)", f"{cond_vol_air_hr:,.6f} m³/hr")
    
    st.info("Squeezing 618 m³/h through the tight 1.81 mm fin gaps creates an air-side friction resistance of 28 Pascals (Pa). To overcome this, the Tecumseh baseplate integrates a 230 mm stamped aluminum axial blade driven by a 10 Watt mechanical output shaft motor spinning at 1300 RPM. This motor draws 32 Watts of electrical input power, matching your electrical spreadsheet balance.")

    st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)

    # Mass Sizing / Tube Volumes
    st.markdown("### Mass & Phase Change Sizing")
    vol_c1, vol_c2 = st.columns(2)
    with vol_c1:
        st.metric("🟢 Total length (m)", f"{cond_tot_len:,.6f} m")
    with vol_c2:
        st.metric("🟢 The Interanl Tube Volume (m³)", f"{cond_int_vol_m3:,.8f} m³")
        st.metric("🟢 The Interanl Tube Volume (cc)", f"{cond_int_vol_cc:,.8f} cc")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    m_c1, m_c2, m_c3 = st.columns(3)
    with m_c1:
        st.caption("The Physics: Hot vapor enters the top rows of the condenser from the compressor at 75°C. The first portion of the coil volume cools this gas down into a saturated vapor at 45°C.")
        st.number_input("Desuperheat Volume (%)", value=st.session_state.cond_desup_pct, key="cond_desup_pct_w", on_change=sync, args=("cond_desup_pct",), step=1.0)
        st.number_input("op (kg/m³)", value=st.session_state.cond_rho_desup, key="cond_rho_desup_w", on_change=sync, args=("cond_rho_desup",), step=0.1)
        st.caption("saturated R134a vapor at these high-temperature nodes has a light density of approximately 52.4 kg/m³ (or 0.0524 g/cc).")
        calc_box("M desuperheat (grams)", m_desup, "g", "{:,.8f}")
        
    with m_c2:
        st.caption("The Physics: This represents the main middle section where the refrigerant undergoes a latent phase change, actively turning from a gas into a liquid at a constant 45°C.")
        st.number_input("Condensing Volume sizes (%)", value=st.session_state.cond_condens_pct, key="cond_condens_pct_w", on_change=sync, args=("cond_condens_pct",), step=1.0)
        st.number_input("z (kg/m³)", value=st.session_state.cond_rho_condens, key="cond_rho_condens_w", on_change=sync, args=("cond_rho_condens",), step=1.0)
        st.caption("Integrated Two-Phase Flow Density: Inside these tubes, a dense liquid film layers the walls while vapor travels down the center core. Applying the industry-standard Premoli void fraction integration, the time-averaged mixed density scales to exactly 330.0 kg/m³.")
        calc_box("Volume sizes (cc)", vol_condens, "cc", "{:,.8f}")
        calc_box("Mass calculation Mcondensing (grams)", m_condens, "g", "{:,.8f}")

    with m_c3:
        st.caption("Pure Liquid Density: Saturated pure liquid R134a at 40°C is dense and heavy, scaling to 1,146 kg/m³.")
        st.number_input("Sub cooling Liquid Zone Vol (%)", value=st.session_state.cond_subcool_pct, key="cond_subcool_pct_w", on_change=sync, args=("cond_subcool_pct",), step=1.0)
        st.number_input("v (kg/m³)", value=st.session_state.cond_rho_subcool, key="cond_rho_subcool_w", on_change=sync, args=("cond_rho_subcool",), step=1.0)
        calc_box("The sub cooling Liquid Zone (cc)", vol_subcool, "cc", "{:,.8f}")
        calc_box("Msubcooling (grams)", m_subcool, "g", "{:,.8f}")

    st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    l_c1, l_c2 = st.columns(2)
    with l_c1:
        st.caption("Mass Calculation: Because this line must be completely packed with 100% solid subcooled liquid at 40°C to feed the valve smoothly, we multiply by the solid liquid density parameter.")
        st.number_input("Using additional connectionto filter and expansion entry (m)", value=st.session_state.cond_line_len, key="cond_line_len_w", on_change=sync, args=("cond_line_len",), step=0.1)
        st.number_input("Liquid line copper tubing(1/4\") (m)", value=st.session_state.cond_line_dia, key="cond_line_dia_w", on_change=sync, args=("cond_line_dia",), step=0.0001, format="%.5f")
        calc_box("Vline (m³)", v_line_m3, "m³", "{:,.8e}")
        calc_box("v1 (cc)", v_line_cc, "cc", "{:,.8f}")
    with l_c2:
        st.number_input("r (kg/m³)", value=st.session_state.cond_rho_line, key="cond_rho_line_w", on_change=sync, args=("cond_rho_line",), step=1.0)
        calc_box("Mtransportline (grams)", m_trans_line, "g", "{:,.8f}")
        
        st.caption("Adding the Filter Drier Core Chamber Inventory: The structural desiccant core chamber inside a commercial liquid filter drier holds an auxiliary liquid volume capacity of exactly 65.5 cc. Because this internal volume is filled with porous solid beads, the space effectively splits, trapping an extra 75.1 grams of solid liquid R134a mass inside the mesh frame.")
        st.number_input("xy (grams) Filter Mass", value=st.session_state.cond_filter_mass, key="cond_filter_mass_w", on_change=sync, args=("cond_filter_mass",), step=1.0)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Final Metric Output
    fin_col, _ = st.columns([1, 1])
    fin_col.metric("🟢 Mhigh side Total (grams)", f"{m_high_side_tot:,.6f} grams")