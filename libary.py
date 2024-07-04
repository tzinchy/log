--renovation.apartments_old_sorted
 SELECT apartments_old.id,
    apartments_old.building_id,
    apartments_old.unkv,
    apartments_old.cad_num,
    apartments_old.apart_type,
    apartments_old.floor,
    apartments_old.area,
    apartments_old.room_count,
    apartments_old.fio,
    apartments_old.people_count,
    apartments_old.requirement,
    apartments_old.old_apart_status,
    apartments_old.notes,
    apartments_old.affair_id,
    apartments_old.kpu_num,
    orders.rd_number,
    orders.rd_date
   FROM renovation.apartments_old
     LEFT JOIN renovation.orders USING (affair_id)
  ORDER BY apartments_old.building_id, (COALESCE("substring"(apartments_old.apart_num::text, '\d+'::text), '0'::text)::integer), apartments_old.id;

--renovation.old_apartments_and_buildings
 WITH apartments_old_sorted AS (
         SELECT apartments_old.id,
            apartments_old.building_id,
            apartments_old.unkv,
            apartments_old.cad_num,
            apartments_old.apart_num,
            apartments_old.apart_type,
            apartments_old.floor,
            apartments_old.area,
            apartments_old.room_count,
            apartments_old.fio,
            apartments_old.people_count,
            apartments_old.old_apart_status,
            apartments_old.rd_num,
            apartments_old.rd_date,
            apartments_old.new_apart_unom,
            apartments_old.new_apart_adress,
            apartments_old.new_apart_num,
            apartments_old.new_apart_room_count,
            apartments_old.new_apart_area,
            apartments_old.new_apart_contract_status,
            apartments_old.new_apart_contract_date,
            apartments_old.notes,
            apartments_old.affair_id,
            apartments_old.kpu_num,
            apartments_old.status,
            apartments_old.new_status
           FROM renovation.apartments_old
          ORDER BY apartments_old.building_id, (COALESCE("substring"(apartments_old.apart_num::text, '\d+'::text), '0'::text)::integer), apartments_old.id
        ), buildings_old_full_view AS (
         SELECT o.id AS buildings_old_id,
            o.unom,
            o.okrug,
            o.district,
            o.adress,
            o.terms_reason,
            t.type,
            d.latest_type AS latest_step,
            d.plan_first_resettlement_start,
            d.plan_first_resettlement_end,
            d.plan_second_resettlement_end,
            d.plan_demolition_end,
            d.actual_first_resettlement_start,
            d.actual_first_resettlement_end,
            d.actual_second_resettlement_end,
            d.actual_demolition_end,
            nc.new_building_ids,
            nc.new_buildings,
            nm.new_building_ids AS moves_to_ids,
            nm.new_buildings AS moves_to,
            COALESCE(at.total, 0::bigint) AS total,
            COALESCE(at.moved, 0::bigint) AS moved,
            COALESCE(at.project, 0::bigint) AS project,
            COALESCE(at.rd, 0::bigint) AS rd,
            COALESCE(at.in_progress, 0::bigint) AS in_progress,
            COALESCE(at.empty, 0::bigint) AS empty
           FROM renovation.buildings_old o
             LEFT JOIN renovation.dates_buildings_old_flat d ON d.building_id = o.id
             LEFT JOIN renovation.buildings_new_flat_construction nc ON nc.old_building_id = o.id
             LEFT JOIN renovation.buildings_new_flat_movement nm ON nm.old_building_id = o.id
             LEFT JOIN renovation.relocation_types t ON t.id = o.relocation_type
             LEFT JOIN ( SELECT apartments_old.building_id,
                    count(*) AS total,
                    count(*) FILTER (WHERE apartments_old.status::text = 'Переселён'::text) AS moved,
                    count(*) FILTER (WHERE apartments_old.status::text = 'Проект договора'::text) AS project,
                    count(*) FILTER (WHERE apartments_old.status::text = 'Распоряжение'::text) AS rd,
                    count(*) FILTER (WHERE apartments_old.status::text = 'В работе'::text) AS in_progress,
                    count(*) FILTER (WHERE apartments_old.status::text = 'Не требуется'::text) AS empty
                   FROM renovation.apartments_old
                  GROUP BY apartments_old.building_id) at ON at.building_id = o.id
          ORDER BY o.okrug, o.district, o.adress
        )
 SELECT aos.id,
    aos.building_id,
    aos.unkv,
    aos.cad_num,
    aos.apart_num,
    aos.apart_type,
    aos.floor,
    aos.area,
    aos.room_count,
    aos.fio,
    aos.people_count,
    aos.old_apart_status,
    aos.rd_num,
    aos.rd_date,
    aos.new_apart_unom,
    aos.new_apart_adress,
    aos.new_apart_num,
    aos.new_apart_room_count,
    aos.new_apart_area,
    aos.new_apart_contract_status,
    aos.new_apart_contract_date,
    aos.notes,
    aos.affair_id,
    aos.kpu_num,
    aos.status,
    aos.new_status,
    bofv.buildings_old_id,
    bofv.unom,
    bofv.okrug,
    bofv.district,
    bofv.adress,
    bofv.terms_reason,
    bofv.type,
    bofv.latest_step,
    bofv.plan_first_resettlement_start,
    bofv.plan_first_resettlement_end,
    bofv.plan_second_resettlement_end,
    bofv.plan_demolition_end,
    bofv.actual_first_resettlement_start,
    bofv.actual_first_resettlement_end,
    bofv.actual_second_resettlement_end,
    bofv.actual_demolition_end,
    bofv.new_building_ids,
    bofv.new_buildings,
    bofv.moves_to_ids,
    bofv.moves_to,
    bofv.total,
    bofv.moved,
    bofv.project,
    bofv.rd,
    bofv.in_progress,
    bofv.empty,
        CASE
            WHEN bofv.actual_first_resettlement_start >= (CURRENT_DATE - '1 mon'::interval) AND bofv.actual_demolition_end IS NULL THEN 'Менее 1 месяца назад'::text
            WHEN bofv.actual_first_resettlement_start >= (CURRENT_DATE - '2 mons'::interval) AND bofv.actual_first_resettlement_start < (CURRENT_DATE - '1 mon'::interval) AND bofv.actual_demolition_end IS NULL AND bofv.actual_first_resettlement_end IS NULL AND bofv.actual_second_resettlement_end IS NULL THEN 'От 1 до 2 месяцев'::text
            WHEN bofv.actual_first_resettlement_start >= (CURRENT_DATE - '5 mons'::interval) AND bofv.actual_first_resettlement_start < (CURRENT_DATE - '2 mons'::interval) AND bofv.actual_demolition_end IS NULL AND bofv.actual_first_resettlement_end IS NULL AND bofv.actual_second_resettlement_end IS NULL THEN 'От 2 до 5 месяцев'::text
            WHEN bofv.actual_first_resettlement_start >= (CURRENT_DATE - '8 mons'::interval) AND bofv.actual_first_resettlement_start < (CURRENT_DATE - '5 mons'::interval) AND bofv.actual_demolition_end IS NULL AND bofv.actual_first_resettlement_end IS NULL AND bofv.actual_second_resettlement_end IS NULL THEN 'От 5 до 8 месяцев'::text
            WHEN bofv.actual_first_resettlement_start < (CURRENT_DATE - '8 mons'::interval) AND bofv.actual_demolition_end IS NULL AND bofv.actual_first_resettlement_end IS NULL AND bofv.actual_second_resettlement_end IS NULL THEN 'Более 8 месяцев'::text
            ELSE NULL::text
        END AS "time"
   FROM apartments_old_sorted aos
     LEFT JOIN buildings_old_full_view bofv ON aos.building_id = bofv.buildings_old_id;

--renovation.buildings_old_full_view
 SELECT o.id,
    o.unom,
    o.okrug,
    o.district,
    o.adress,
    o.terms_reason,
    t.type,
    d.latest_type AS latest_step,
    d.plan_first_resettlement_start,
    d.plan_first_resettlement_end,
    d.plan_second_resettlement_end,
    d.plan_demolition_end,
    d.actual_first_resettlement_start,
    d.actual_first_resettlement_end,
    d.actual_second_resettlement_end,
    d.actual_demolition_end,
    nc.new_building_ids,
    nc.new_buildings,
    nm.new_building_ids AS moves_to_ids,
    nm.new_buildings AS moves_to,
    COALESCE(at.total, 0::bigint) AS total,
    COALESCE(at.moved, 0::bigint) AS moved,
    COALESCE(at.project, 0::bigint) AS project,
    COALESCE(at.rd, 0::bigint) AS rd,
    COALESCE(at.in_progress, 0::bigint) AS in_progress,
    COALESCE(at.empty, 0::bigint) AS empty
   FROM renovation.buildings_old o
     LEFT JOIN renovation.dates_buildings_old_flat d ON d.building_id = o.id
     LEFT JOIN renovation.buildings_new_flat_construction nc ON nc.old_building_id = o.id
     LEFT JOIN renovation.buildings_new_flat_movement nm ON nm.old_building_id = o.id
     LEFT JOIN renovation.relocation_types t ON t.id = o.relocation_type
     LEFT JOIN ( SELECT apartments_old.building_id,
            count(*) AS total,
            count(*) FILTER (WHERE apartments_old.status::text = 'Переселён'::text) AS moved,
            count(*) FILTER (WHERE apartments_old.status::text = 'Проект договора'::text) AS project,
            count(*) FILTER (WHERE apartments_old.status::text = 'Распоряжение'::text) AS rd,
            count(*) FILTER (WHERE apartments_old.status::text = 'В работе'::text) AS in_progress,
            count(*) FILTER (WHERE apartments_old.status::text = 'Не требуется'::text) AS empty
           FROM renovation.apartments_old
          GROUP BY apartments_old.building_id) at ON at.building_id = o.id
  ORDER BY o.okrug, o.district, o.adress;
