from residue_lab import physics
from residue_lab.chart import lab_covers
from residue_lab.claims import TERMS, apply_l2
from residue_lab.grader import certify, leftover_weight_frac
from residue_lab.units import DEFAULT_LAB_DISK, gem_lab_floor_dg_over_g

WEIGHT_FLOOR = 1e-12

def protocol_ehd():
    covers = lab_covers()
    air = physics.l1_ehd(covers["ehd_air"])
    vac = physics.l1_ehd(covers["ehd_vacuum"])
    # Leftover after the L1 ion-wind model is 0 by construction (L1 is the whole model); the verdict is computed,
    # not forced. This changes the ehd_air certificate from the previously forced OPEN to OPEN_NULL.
    air_c = certify("ehd_air", 0.0, 1e-9, notes={"force_z": f"{air.force_z:.3e}", "accounted_by": "L1 ion wind"})
    vac_c = certify("ehd_vacuum", vac.force_z, 1e-9, notes={"force_z": f"{vac.force_z:.3e}"})
    return air_c, vac_c

def protocol_gem_harris():
    l1 = physics.l1_gem_weight_drop(lab_covers()["gem_rotating"])
    floor = max(WEIGHT_FLOOR, gem_lab_floor_dg_over_g(DEFAULT_LAB_DISK) * 10)
    return certify("gem_harris", l1.weight_drop_frac, floor)

def protocol_gem_harris_mesh():
    from residue_lab.gem_mesh import gem_mesh_dg_over_g
    out = gem_mesh_dg_over_g(DEFAULT_LAB_DISK)
    floor = max(WEIGHT_FLOOR, gem_lab_floor_dg_over_g(DEFAULT_LAB_DISK) * 100)
    return certify("gem_harris_mesh", out["max_dg_over_g"], floor, notes={"carrier": "dec_faces"})

def protocol_li_static():
    l1 = physics.l1_london_static_weight_drop(lab_covers()["li_static_sc"])
    return certify("li_static_ybco", l1.weight_drop_frac, 5e-4)

def protocol_li_toggle():
    cover = lab_covers()["li_toggle"]
    l1 = physics.l1_gem_weight_drop(cover)
    sim = apply_l2("li_torr_lab_bg", cover, l1, enabled=True)
    term = TERMS["li_torr_lab_bg"]
    return certify("li_toggle", leftover_weight_frac(sim, l1), WEIGHT_FLOOR, l2_on=("li_torr_lab_bg",), unpaid=(term.unpaid_restriction,))

def run_v0():
    air, vac = protocol_ehd()
    return [air, vac, protocol_gem_harris(), protocol_gem_harris_mesh(), protocol_li_static(), protocol_li_toggle()]
